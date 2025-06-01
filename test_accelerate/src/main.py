# encoding: utf-8

import os
import time
import numpy as np
from multiprocessing import Process, Lock
from tqdm import tqdm
import torch
from torch.utils.data import Dataset, DataLoader, DistributedSampler
from torch.optim import SGD
from torch import nn
from accelerate import Accelerator


class DummyDataset(Dataset):
    """简单数据集

    数据：[(x1, x2), (y)]

    """

    def __init__(self, n_samples, rank):
        super().__init__()
        self.rank_interval = 1000000
        assert (
            n_samples <= self.rank_interval
        ), f"too large n_samples {n_samples} > {self.rank_interval}"
        self.n_samples = n_samples
        self.rank = rank
        self.rank_step = self.rank * self.rank_interval

    def __len__(self):
        return self.n_samples

    def __getitem__(self, index):
        features = np.array([index + self.rank_step, index + self.rank_step + 0.5])
        labels = np.array([index % 2])
        features = features.astype(np.float32)
        labels = labels.astype(np.int64)
        return (torch.from_numpy(features), torch.from_numpy(labels))


class DummyNet(nn.Module):
    """简单网络"""

    def __init__(self, input_dim, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 2)
        self.sm = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.sm(x)
        return x


def main():
    # rank = os.environ.get("RANK")
    # if rank is None:
    #     rank = 0
    # 创建accelerator对象
    accelerator = Accelerator()
    rank = accelerator.process_index
    world_size = accelerator.num_processes

    # 只在当前机器的主进程执行
    if accelerator.is_local_main_process:
        print(f"rank={rank}, world_size={world_size}")

    # 创建进程锁
    lock = Lock()

    # 设置模型参数保存路径
    save_path = f"./output/test-{rank}.pt"
    # 检查目录是否存在，不存在则创建
    if accelerator.is_local_main_process:  # 只在主进程运行
        if not os.path.isdir(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

    # 创建数据集
    dataset = DummyDataset(16, rank=rank)
    print(f"rank={rank}, dataset[0]={dataset[0]}, dataset[100]={dataset[100]}")

    # 创建数据加载器
    data_loader = DataLoader(dataset, batch_size=4, shuffle=False)

    # 创建模型
    model = DummyNet(input_dim=2)
    # 载入模型
    if accelerator.is_main_process and os.path.isfile(save_path):
        model.load_state_dict(torch.load(save_path, weights_only=True))
        accelerator.print(f"load weights from {save_path}")

    # 创建优化器
    optimizer = torch.optim.Adam(model.parameters())

    # 使用accelerate修饰
    acc_loader = accelerator.prepare(data_loader)  # 会自动分片
    acc_model = accelerator.prepare(model)
    acc_optimizer = accelerator.prepare(optimizer)

    # 进度条设置只在主进程中显示，可以用rank或者is_local_main_process两种方式判断
    for epoch in tqdm(range(2), desc="training", disable=(not rank == 0)):
        all_loss = []

        # for idx, batch in enumerate(data_loader): # 用于不需要分片的情况
        for idx, batch in enumerate(acc_loader):  # 用于按进程数分片的情况
            accelerator.print(f"iter: {idx}")
            with lock:
                print(f"rank={rank}", f"idx={idx}", f"batch={batch[0]}", flush=True)

            # 梯度清零
            acc_optimizer.zero_grad()

            # 前向推理
            feat, lbl = batch[0], batch[1]
            prob = acc_model(feat)

            # 计算损失
            lbl = lbl.squeeze(dim=-1)
            accelerator.print(f"prob.shape={prob.shape}, lbl.shape={lbl.shape}")
            loss = torch.nn.functional.cross_entropy(prob, lbl)

            # 误差反传
            accelerator.backward(loss)
            acc_optimizer.step()
            #
            all_loss.append(loss.detach().cpu())
            time.sleep(1)

        # 收集所有进程的数据
        all_loss = torch.stack(all_loss)
        all_loss = all_loss.unsqueeze(dim=0)
        accelerator.print(f"main process mean_loss={all_loss}")
        all_loss = accelerator.gather(
            all_loss
        )  # 会将多个进程的数据在dim=0的维度上拼接起来
        if accelerator.is_local_main_process:
            print(f"gather mean_loss={all_loss}")

    # 等待所有进程到这里
    accelerator.wait_for_everyone()

    # 保存模型参数
    # 只在主机器上的主进程执行，单机情况下与is_local_main_process没有区别
    if accelerator.is_main_process:
        # 解包分布式模型为本地模型
        unwrapped_model = accelerator.unwrap_model(acc_model)
        # 保存到文件
        accelerator.save(unwrapped_model.state_dict(), save_path)


if __name__ == "__main__":
    main()

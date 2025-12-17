# -*- coding: utf-8 -*-
"""
@Author: Lyu Jie
@Time: 2025-12-17 14:14:36
@File: q_learning.py
@Project:
@Description: 参考 [Reinforcement Learning (DQN) Tutorial](https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)
"""

import argparse
import os
import gymnasium as gym
import math
import random
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

# Q网络相关
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# 采样数据的存储结构
Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))


class ReplayMemory(object):
    """经验回放的存储结构"""

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    """Q网络：用于根据当前状态预测动作"""

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)


# if GPU is to be used
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)
# 模型路径
model_path = "output/q.pt"


def train():
    """训练"""
    env = gym.make("CartPole-v1")
    plt.ion()
    # 训练参数设置
    BATCH_SIZE = 128  # 一次采样的样本数
    GAMMA = 0.99  # 折扣率
    EPS_START = 0.9  # \epsilon 贪心策略的参数
    EPS_END = 0.05  # \epsilon 贪心策略的参数
    EPS_DECAY = 1000  # \epsilon 贪心策略的参数
    TAU = 0.005  # 目标网络的更新率
    LR = 1e-4  # 学习率
    # 获取动作个数
    n_actions = env.action_space.n
    # 获取观测到的状态维度数
    state, info = env.reset()
    n_observations = len(state)
    # 创建策略网络和目标网络
    policy_net = DQN(n_observations, n_actions).to(device)
    target_net = DQN(n_observations, n_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())
    # 创建优化器
    optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
    # 创建经验回放的存储结构
    memory = ReplayMemory(10000)
    # 设置训练的回合数
    num_episodes = 1200
    # 采样计数器
    steps_done = 0

    def select_action(state):
        """使用策略产生动作"""
        nonlocal steps_done
        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(
            -1.0 * steps_done / EPS_DECAY
        )
        steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                # 预测
                return policy_net(state).max(1).indices.view(1, 1)
        else:
            return torch.tensor(
                [[env.action_space.sample()]], device=device, dtype=torch.long
            )

    episode_durations = []

    def plot_durations(show_result=False):
        """绘制持续时长的图"""
        plt.figure(1)
        durations_t = torch.tensor(episode_durations, dtype=torch.float)
        if show_result:
            plt.title("Result")
        else:
            plt.clf()
            plt.title("Training...")
        plt.xlabel("Episode")
        plt.ylabel("Duration")
        plt.plot(durations_t.numpy())
        # Take 100 episode averages and plot them too
        if len(durations_t) >= 100:
            means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
            means = torch.cat((torch.zeros(99), means))
            plt.plot(means.numpy())

        plt.pause(0.001)  # pause a bit so that plots are updated

    def optimize_model():
        """进行一次模型参数的优化迭代"""
        if len(memory) < BATCH_SIZE:
            return
        # 采样
        transitions = memory.sample(BATCH_SIZE)
        # 准备当前一批样本数据
        batch = Transition(*zip(*transitions))
        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.next_state)),
            device=device,
            dtype=torch.bool,
        )
        non_final_next_states = torch.cat(
            [s for s in batch.next_state if s is not None]
        )
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        # 计算 q(s_t, a)
        state_action_values = policy_net(state_batch).gather(1, action_batch)
        # 计算 \hat{q}(s_{t+1})
        next_state_values = torch.zeros(BATCH_SIZE, device=device)
        with torch.no_grad():
            next_state_values[non_final_mask] = (
                target_net(non_final_next_states).max(1).values
            )
        # 计算价值的期望 r + \gamma * \hat{q}(s_{t+1})
        expected_state_action_values = (next_state_values * GAMMA) + reward_batch
        # 计算Huber损失
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))
        # 优化
        optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
        optimizer.step()

    # 经验回放的采样和训练
    for i_episode in range(num_episodes):
        # 环境初始化
        state, info = env.reset()
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        for t in count():
            action = select_action(state)
            observation, reward, terminated, truncated, _ = env.step(action.item())
            reward = torch.tensor([reward], device=device)
            done = terminated or truncated
            # 判断终止条件
            if terminated:
                next_state = None
            else:
                next_state = torch.tensor(
                    observation, dtype=torch.float32, device=device
                ).unsqueeze(0)
            # 存储状态转移的数据
            memory.push(state, action, next_state, reward)
            # 下一步状态
            state = next_state
            # 优化模型
            optimize_model()
            # 更新目标网络
            # θ′ ← τ θ + (1 −τ )θ′
            target_net_state_dict = target_net.state_dict()
            policy_net_state_dict = policy_net.state_dict()
            for key in policy_net_state_dict:
                target_net_state_dict[key] = policy_net_state_dict[
                    key
                ] * TAU + target_net_state_dict[key] * (1 - TAU)
            target_net.load_state_dict(target_net_state_dict)
            # 完成状态
            if done:
                episode_durations.append(t + 1)
                plot_durations()
                break
    # 训练结束
    print("Complete")
    plot_durations(show_result=True)
    plt.ioff()
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    torch.save(target_net.state_dict(), model_path)
    plt.show()


def test():
    """测试模型效果"""
    # 创建环境
    env = gym.make("CartPole-v1", render_mode="human")
    # 获取动作个数
    n_actions = env.action_space.n
    # 获取观测到的状态维度
    state, info = env.reset()
    n_observations = len(state)
    # 创建Q网络
    target_net = DQN(n_observations, n_actions).to(device)
    assert os.path.isfile(model_path), f"not found {model_path}"
    target_net.load_state_dict(torch.load(model_path))
    for i_episode in range(100):
        # 初始化环境
        state, info = env.reset()
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        for t in count():
            with torch.no_grad():
                # t.max(1) will return the largest column value of each row.
                # second column on max result is index of where max element was
                # found, so we pick action with the larger expected reward.
                action = target_net(state).max(1).indices.view(1, 1)
            # 执行动作
            observation, reward, terminated, truncated, _ = env.step(action.item())
            reward = torch.tensor([reward], device=device)
            # 检查终止标志
            done = terminated or truncated
            if terminated:
                next_state = None
            else:
                next_state = torch.tensor(
                    observation, dtype=torch.float32, device=device
                ).unsqueeze(0)
            # 转移到下一步
            state = next_state
            if done:
                break
        print(f"episode: {i_episode+1}, duration: {t+1}")
    print("done.")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="处理不同阶段的程序")

    # 添加 phase 参数
    parser.add_argument(
        "phase",  # 长参数名
        type=str,  # 参数类型
        choices=["train", "test", "eval", "inference"],  # 允许的值
        default="train",  # 默认值
        help="运行阶段: train, test, eval, inference (默认: train)",
    )

    # 解析参数
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.phase == "train":
        train()
    elif args.phase == "test":
        test()
    else:
        raise ValueError(f"未知参数 phase={args.phase}")


if __name__ == "__main__":
    main()

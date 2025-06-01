# 初试 accelerate 多进程

[github](https://github.com/huggingface/accelerate)

## 安装 

```shell
pip install accelerate
```

## 单进程运行

```shell
python src/main.py
```

## 多进程运行

```shell
accelerate launch --multi_gpu --num_processes 2 src/main.py
```

## 指定配置文件运行

```shell
accelerate launch --config_file accelerate_config.yaml src/main.py
```

如果调用脚本需要传入命令行参数，就跟在后面，与运行普通脚本一样

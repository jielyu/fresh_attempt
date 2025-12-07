# 测试uv管理python环境

## 运行指令

### 创建功能

```
uv init test_uv
```

### 创建虚拟环境

```
uv venv -p 3.12
```

### 运行脚本

```
uv run main.py
```

### 安装工具

```
uv add --dev pip
```

### 查看安装包

```
uv pip list
```

### 激活虚拟环境

```
source .venv/bin/activate
```

**注意：** 进入虚拟环境后的操作可能会修改主机环境，需要严格确认指令为虚拟环境中的指令


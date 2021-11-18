# 打包Python程序为可执行文件的步骤

## 1. 第一步创建虚拟环境

```shell
virtualenv pkg_env -p python3
```

## 2. 在虚拟环境中安装pyinstaller

```shell
source ./pkg_env/bin/activate
```

```shell
pip install pyinstaller
```

## 3. 打包Python程序

```shell
./pkg_env/bin/pyinstaller test.py
```

在当前目录下的 `dist` 目录下就可以见到打包好的程序了。

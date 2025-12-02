#!/bin/bash

set -ex

echo "Building TorchVision test..."

# 清理并创建构建目录
rm -rf build
mkdir build
cd build

# 设置 libtorch 路径（根据你的安装位置修改）
export Torch_DIR=$HOME/Libraries/libtorch/share/cmake/Torch
export TorchVision_DIR=$HOME/Libraries/libtorchvision/share/cmake/TorchVision  # 如果从源码编译

# 运行 CMake
cmake -DCMAKE_PREFIX_PATH="$Torch_DIR;$TorchVision_DIR" ..

# 编译
make

# 运行测试
echo -e "\nRunning test..."
./test_torchvision

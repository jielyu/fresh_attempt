cmake_minimum_required(VERSION 3.18)
project(test_torchvision)

set(CMAKE_CXX_STANDARD 17)

# 查找 Torch 和 TorchVision
find_package(Torch REQUIRED)
find_package(TorchVision REQUIRED)

# 添加可执行文件
add_executable(test_torchvision src/main.cpp)

# 链接库
target_link_libraries(test_torchvision 
    ${TORCH_LIBRARIES}
    TorchVision::TorchVision
)

# 设置包含目录
target_include_directories(test_torchvision PRIVATE ${TORCH_INCLUDE_DIRS} ${TorchVision_INCLUDE_DIR})

# 如果需要调试信息
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0")

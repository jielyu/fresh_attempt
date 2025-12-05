cmake_minimum_required(VERSION 3.10)
project(test_trt)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找包
find_package(OpenCV REQUIRED)
find_package(CUDA REQUIRED)

# 设置TensorRT路径（根据你的安装位置调整）
set(TENSORRT_ROOT "$ENV{HOME}/Libraries/TensorRT-10.14.1.48" CACHE PATH "TensorRT安装路径")

# 查找TensorRT
find_path(TENSORRT_INCLUDE_DIR NvInfer.h
          PATHS ${TENSORRT_ROOT}/include
          NO_DEFAULT_PATH)
          
find_library(TENSORRT_LIBRARY NAMES nvinfer
             PATHS ${TENSORRT_ROOT}/lib
             NO_DEFAULT_PATH)
             
find_library(TENSORRT_PARSER_LIBRARY NAMES nvonnxparser
             PATHS ${TENSORRT_ROOT}/lib
             NO_DEFAULT_PATH)

# 包含目录
include_directories(
    ${OpenCV_INCLUDE_DIRS}
    ${CUDA_INCLUDE_DIRS}
    ${TENSORRT_INCLUDE_DIR}
)
message(STATUS OpenCV_INCLUDE_DIRS:${OpenCV_INCLUDE_DIRS})
message(STATUS CUDA_INCLUDE_DIRS:${CUDA_INCLUDE_DIRS})
message(STATUS TENSORRT_INCLUDE_DIR:${TENSORRT_INCLUDE_DIR})

# 添加可执行文件
add_executable(${PROJECT_NAME} src/main.cpp)

# 链接库
target_link_libraries(${PROJECT_NAME}
    ${OpenCV_LIBS}
    ${CUDA_LIBRARIES}
    ${TENSORRT_LIBRARY}
    ${TENSORRT_PARSER_LIBRARY}
    # cudart
)

# CUDA配置
# if(CUDA_FOUND)
#     set(CUDA_NVCC_FLAGS ${CUDA_NVCC_FLAGS} -std=c++14)
# endif()
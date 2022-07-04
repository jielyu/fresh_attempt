cmake_minimum_required(VERSION 3.0.0)
project(test_libtorch)

set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} /usr/local/Cellar/opencv/4.5.4_1)
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} /usr/local/libtorch/v1.12.0)

# 配置OpenCV
find_package(OpenCV 4.5.4 REQUIRED)

# 配置LibTorch
include_directories(${CMAKE_PREFIX_PATH}/include)
include_directories(${CMAKE_PREFIX_PATH}/include/torch/csrc/api/include)
find_package(Torch REQUIRED)
message(STATUS "OpenCV version: ${OpenCV_VERSION}")
message(STATUS "OpenCV: ${OpenCV_LIBS}")
message(STATUS "Torch: ${TORCH_LIBRARIES}")

set(CMAKE_CXX_STANDARD 14)

# 生成目标
add_executable(${PROJECT_NAME} src/main.cpp)
target_link_libraries(${PROJECT_NAME} "${TORCH_LIBRARIES}" "${OpenCV_LIBS}")

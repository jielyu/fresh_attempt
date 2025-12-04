cmake_minimum_required(VERSION 3.5)
project(test_onnx)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
message(STATUS OpenCV_INCLUDE_DIRS:${OpenCV_INCLUDE_DIRS})

find_package(CUDA REQUIRED)
include_directories(${CUDA_INCLUDE_DIRS})
message(STATUS CUDA_INCLUDE_DIRS:${CUDA_INCLUDE_DIRS})
add_definitions(-DUSE_CUDA)

set(ONNXRUNTIME_ROOT "$ENV{HOME}/Libraries/onnxruntime-linux-x64-gpu-1.23.2")
include_directories(${PROJECT_NAME} ${ONNXRUNTIME_ROOT}/include)

set(PROJECT_SOURCES src/main.cpp)
add_executable(${PROJECT_NAME} ${PROJECT_SOURCES})

target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS} ${ONNXRUNTIME_ROOT}/lib/libonnxruntime.so)
target_link_libraries(${PROJECT_NAME} ${CUDA_LIBRARIES})

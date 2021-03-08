cmake_minimum_required(VERSION 2.8.12)
project(demo)

set(OpenCV_DIR "/usr/local/Cellar/opencv/4.2.0_3/lib/cmake/opencv4/")
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
add_definitions(-std=c++11)

add_executable(demo demo.cpp)
target_link_libraries(demo ${OpenCV_LIBS})

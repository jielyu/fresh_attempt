cmake_minimum_required(VERSION 2.8.12)
project(demo)

find_package(gflags REQUIRED)
include_directories(${gflags_INCLUDE_DIR})
set(gflags_LIB gflags)
message(STATUS "gflags_INCLUDE_DIR=${gflags_INCLUDE_DIR}, gflags_LIB=${gflags_LIB}")

add_definitions(-std=c++11)

add_executable(demo demo.cpp)
target_link_libraries(demo ${gflags_LIB})

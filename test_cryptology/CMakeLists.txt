cmake_minimum_required(VERSION 3.10)
project(crypt_impl)

#config compiler
set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}  -std=c++11")

# find all source files
aux_source_directory(src SRC_FILES)
message(STATUS "source files: ${SRC_FILES}")

# config target
add_executable(${PROJECT_NAME} ${SRC_FILES})
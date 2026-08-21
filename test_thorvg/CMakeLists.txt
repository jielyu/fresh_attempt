cmake_minimum_required(VERSION 3.16)
project(thorvg_boolean_demo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(thorvg REQUIRED)
find_package(clipper2 REQUIRED)
find_package(PNG REQUIRED)

add_executable(path_boolean src/main.cpp)

target_link_libraries(path_boolean PRIVATE
    thorvg::thorvg
    clipper2::clipper2
    PNG::PNG
)

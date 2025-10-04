cmake_minimum_required(VERSION 3.15)
project(example LANGUAGES CXX)

# 使用 Conan 生成的工具链和依赖
list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

find_package(pybind11 REQUIRED CONFIG)
find_package(nlohmann_json REQUIRED CONFIG)
find_package(pybind11_json REQUIRED CONFIG)

file(GLOB_RECURSE MODULE_SOURCES "src/*.cpp")
list(FILTER MODULE_SOURCES EXCLUDE REGEX "src/json\\.cpp$")

pybind11_add_module(example ${MODULE_SOURCES})

# 设置 C++ 标准（pybind11 需要 C++11 或更高）
target_compile_features(example PRIVATE cxx_std_17)

target_link_libraries(${PROJECT_NAME} PRIVATE 
    pybind11::module 
    nlohmann_json::nlohmann_json 
    pybind11_json::pybind11_json
)

# 可选：复制模块到源码测试目录，便于测试
add_custom_command(TARGET example POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:example> ${CMAKE_SOURCE_DIR}/test/
    COMMENT "Copying module to test directory"
)
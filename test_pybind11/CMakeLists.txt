cmake_minimum_required(VERSION 3.15)
project(example LANGUAGES CXX)

# 使用 Conan 生成的工具链和依赖
list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

find_package(pybind11 REQUIRED CONFIG)
find_package(nlohmann_json REQUIRED CONFIG)
find_package(pybind11_json REQUIRED CONFIG)
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    message(STATUS "Running on Linux")
    # 添加 Linux 特定的配置
    find_package(OpenMP REQUIRED)
endif()

file(GLOB_RECURSE MODULE_SOURCES "src/*.cpp")
# list(FILTER MODULE_SOURCES EXCLUDE REGEX "src/json\\.cpp$")

pybind11_add_module(example ${MODULE_SOURCES})

# 设置 C++ 标准（pybind11 需要 C++11 或更高）
target_compile_features(example PRIVATE cxx_std_17)

# target_link_libraries(${PROJECT_NAME} PRIVATE 
#     pybind11::module 
#     nlohmann_json::nlohmann_json 
#     pybind11_json::pybind11_json
# )

if(APPLE)
    # 避免重复链接 C++ 标准库
    # set(CMAKE_CXX_STANDARD_LIBRARIES "")
    # 或者明确指定
    # set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++")
    target_compile_options(${PROJECT_NAME} PRIVATE -Xpreprocessor -fopenmp)
    if(CMAKE_SYSTEM_PROCESSOR MATCHES "arm64|aarch64")
        message(STATUS "Running on Apple Silicon (ARM)")
        include_directories(/opt/homebrew/Cellar/libomp/18.1.8/include)
        target_link_libraries(${PROJECT_NAME} PUBLIC 
            "/opt/homebrew/Cellar/libomp/18.1.8/lib/libomp.dylib" 
            pybind11::module 
            nlohmann_json::nlohmann_json 
            pybind11_json::pybind11_json
        )
    elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
        message(STATUS "Running on Intel x86_64")
        include_directories(/usr/local/Cellar/libomp/18.1.7/include)
        target_link_libraries(${PROJECT_NAME} PUBLIC 
            "/usr/local/Cellar/libomp/18.1.7/lib/libomp.dylib" 
            pybind11::module 
            nlohmann_json::nlohmann_json 
            pybind11_json::pybind11_json
        )
    else()
        message(FATAL_ERROR "Unknown CPU architecture: ${CMAKE_SYSTEM_PROCESSOR}")
    endif()
    
else()
    target_link_libraries(${PROJECT_NAME} OpenMP::OpenMP_CXX pybind11::module nlohmann_json::nlohmann_json pybind11_json::pybind11_json)
endif()

# 可选：复制模块到源码测试目录，便于测试
add_custom_command(TARGET example POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:example> ${CMAKE_SOURCE_DIR}/test/
    COMMENT "Copying module to test directory"
)
cmake_minimum_required(VERSION 3.16)
project(GlfwVulkan)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 GLFW（通过 pkg-config 或系统路径）
find_package(glfw3 REQUIRED)
find_package(glm REQUIRED)

# 查找 Vulkan
find_package(Vulkan REQUIRED)

# 包含头文件（通常不需要，GLFW 和 Vulkan 已安装在系统路径）
include_directories(${Vulkan_INCLUDE_DIRS})

# 添加可执行文件
add_executable(vulkan_window src/main.cpp)

# 链接库
target_link_libraries(vulkan_window PRIVATE glfw glm::glm ${Vulkan_LIBRARIES})
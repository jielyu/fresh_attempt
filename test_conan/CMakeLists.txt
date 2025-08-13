cmake_minimum_required(VERSION 3.15)
project(test_conan)

# 设置依赖库
find_package(glog REQUIRED)
find_package(gflags REQUIRED)
find_package(OpenCV REQUIRED)
find_package(xtensor REQUIRED)

aux_source_directory(src SOURCES)
add_executable(${PROJECT_NAME} ${SOURCES})

# 链接 Glog
target_link_libraries(${PROJECT_NAME} glog::glog gflags::gflags ${OpenCV_LIBS} xtensor)
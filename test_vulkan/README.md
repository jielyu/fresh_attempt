# Vulkan示例

## 安装依赖库

```shell
conan install .
```

## 编译

```shell
cmake .. -DCMAKE_TOOLCHAIN_FILE=Release/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
```

## 运行

```shell
./build/vulkan_window
```
# pybind11 案例

使用pybind11提供Python可调用的C++接口，用于需要C++加速的Python开发场景

## 编译

```shell
conan build . --build=missing
```

## 运行测试

```shell
python3 test/test.py
```
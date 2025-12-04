# onnx-gpu调用演示

**仅用于演示，实际工程实现还需要更慎重地处理**

## 运行

### Python

```
python python/main.py
```

### C++

```
mkdir -p build && cd build
cmake ..
make
./test_onnx
```

## 依赖

```
cmake
opencv
cuda
onnx-gpu
```
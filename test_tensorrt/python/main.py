# encoding: utf-8

import tensorrt as trt

import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import cv2

import tensorrt as trt


def build_engine(
    onnx_path: str,
    engine_path: str,
    fp16: bool = True,
    input_shape: tuple = (1, 3, 640, 640),
):
    """将ONNX模型转换为TensorRT引擎"""
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(
        1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    )
    parser = trt.OnnxParser(network, TRT_LOGGER)

    # 解析ONNX模型
    with open(onnx_path, "rb") as model:
        if not parser.parse(model.read()):
            for error in range(parser.num_errors):
                print(parser.get_error(error))
            return None

    # 配置构建器
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)  # 1GB

    if fp16 and builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)

    # 构建引擎
    serialized_engine = builder.build_serialized_network(network, config)

    # 保存引擎
    with open(engine_path, "wb") as f:
        f.write(serialized_engine)

    print(f"引擎已保存到: {engine_path}")
    return serialized_engine


# 使用示例
# build_engine("yolov8n.onnx", "yolov8n.trt")


def main():
    pass
    # build_engine("../test_onnx/models/best.onnx", "./output/best.trt")

    # 配置参数
    ENGINE_PATH = "output/best.trt"  # 你的TensorRT引擎文件
    # 载入模型
    print("读取模型 {}".format(ENGINE_PATH))
    logger = trt.Logger(trt.Logger.ERROR)
    with open(ENGINE_PATH, "rb") as f, trt.Runtime(logger) as runtime:
        assert runtime
        engine = runtime.deserialize_cuda_engine(f.read())
    assert engine
    context = engine.create_execution_context()
    assert context

    # 设置输入输出的内存绑定
    inputs = []
    outputs = []
    device_buffers = []
    for i in range(engine.num_io_tensors):
        name = engine.get_tensor_name(i)
        dtype = engine.get_tensor_dtype(name)
        shape = engine.get_tensor_shape(name)
        size = np.dtype(trt.nptype(dtype)).itemsize  # 计算TensorRT数据类型所占字节数
        for s in shape:
            size *= s  # 计算内存大小
        device_buffer = cuda.mem_alloc(size)
        device_buffers.append(device_buffer)
        binding = {
            "index": i,
            "name": name,
            "dtype": np.dtype(trt.nptype(dtype)),
            "shape": list(shape),
            "device_buffer": device_buffer,
        }
        if engine.get_tensor_mode(name) == trt.TensorIOMode.INPUT:
            inputs.append(binding)
        else:
            outputs.append(binding)
    print(inputs, outputs)

    # 运行
    output = np.zeros(outputs[0]["shape"], dtype=outputs[0]["dtype"])
    print(output.shape)
    input_t = np.zeros(inputs[0]["shape"], dtype=inputs[0]["dtype"])
    cuda.memcpy_htod_async(inputs[0]["device_buffer"], np.ascontiguousarray(input_t))
    context.execute_v2(device_buffers)
    cuda.memcpy_dtoh_async(output, outputs[0]["device_buffer"])
    print(output)


if __name__ == "__main__":
    main()

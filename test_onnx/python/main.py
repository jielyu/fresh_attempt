# encoding: utf-8

import os
import numpy as np
import onnxruntime as ort


def main():

    onnx_model_path = "models/best.onnx"
    assert os.path.isfile(onnx_model_path), f"not found {onnx_model_path}"

    # 创建会话
    session = ort.InferenceSession(
        onnx_model_path, providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
    )
    # 获取输入
    model_inputs = session.get_inputs()
    input_shape = model_inputs[0].shape
    input_name = model_inputs[0].name
    print(input_name, input_shape)
    # 构建数据
    img = np.zeros((input_shape[3], input_shape[2], 3), dtype=np.uint8)
    # 预处理
    image_data = np.array(img) / 255.0
    image_data = np.transpose(image_data, (2, 0, 1))
    image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
    # 运行
    outputs = session.run(None, {input_name: image_data})
    #
    print(f"n_out: {len(outputs)}")
    print(outputs[0].shape)


if __name__ == "__main__":
    main()

/*
参考教程： https://juejin.cn/post/6986819804757753869
*/

#include <torch/script.h> // 引入libtorch头文件
#include <torch/torch.h>  // cuda相关函数头文件

#include <opencv2/opencv.hpp>
using namespace std;

int main()
{
    //确定当前设备类型（CPU或GPU）
    torch::DeviceType device_type = at::kCPU; // 定义设备类型
    if (torch::cuda::is_available())
        device_type = at::kCUDA;

    // 加载抠图模型
    std::string model_path = "../models/photo_sketch.pt"; // 模型路径
    torch::jit::script::Module model;
    try
    {
        model = torch::jit::load(model_path); //加载模型
    }
    catch (const c10::Error &e)
    {
        cout << "无法加载模型" << endl;
        return -1;
    }
    // model.eval();
    model.to(device_type);
    cout << "成功加载模型" << endl;

    // 加载图片
    std::string img_path = "../data/Valley-Taurus-Mountains-Turkey.jpg"; // 图片路径
    cv::Mat img = cv::imread(img_path);                                  // 读取图片

    //数据预处理
    std::vector<int64_t> sizes = {1, img.rows, img.cols, 3};
    at::TensorOptions options(at::ScalarType::Byte);
    at::Tensor tensor_image = torch::from_blob(img.data, at::IntList(sizes), options); //将opencv的图像数据转为Tensor张量数据
    tensor_image = tensor_image.toType(at::kFloat);                                    //转为浮点型张量数据

    tensor_image = tensor_image.permute({0, 3, 1, 2});
    tensor_image[0][0] = tensor_image[0][0].sub(114).div(255.0);
    tensor_image[0][1] = tensor_image[0][1].sub(121).div(255.0);
    tensor_image[0][2] = tensor_image[0][2].sub(134).div(255.0);
    tensor_image = tensor_image.to(device_type);
    cout << "图片预处理完成" << endl;

    // 推理
    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(tensor_image);
    at::Tensor out_tensor = model.forward(inputs).toTensor();
    cout << "推理完成" << endl;

    // 后处理
    out_tensor = out_tensor.squeeze().detach();
    out_tensor = out_tensor.add(1.0).div(2.0).mul(255).clamp_(0, 255).to(torch::kU8);
    out_tensor = out_tensor.to(torch::kCPU);
    cout << "后处理完成" << endl;

    // 格式转换 tensor -> cv::Mat
    cout << "tensor, h:" << out_tensor.size(0) << ";w:" << out_tensor.size(1) << endl;
    cv::Mat sketch_img(out_tensor.size(0), out_tensor.size(1), CV_8UC1);
    std::memcpy((void *)sketch_img.data, out_tensor.data_ptr(), sizeof(torch::kU8) * out_tensor.numel());
    cout << "结果数据格式转换完成" << endl;

    // 显示结果
    cv::imshow("sketch", sketch_img);
    cv::imwrite("../sketch.jpg", sketch_img);
    cout << "保存到：../sketch.jpg" << endl;
    cv::waitKey(0);

    return 0;
}
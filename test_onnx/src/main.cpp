/** 用于演示onnx-gpu调用的情况
 * 
 * 参考： https://github.com/sunsmarterjie/yolov12.git  examples/YOLOv8-ONNXRuntime-CPP
 * 
 * 注意： 仅用于演示，实际工程实现还需要更慎重地处理
 * 
*/

#include <iostream>

#include <string>
#include <vector>
#include <cstdio>
#include <opencv2/opencv.hpp>
#include "onnxruntime_cxx_api.h"

#define    RET_OK nullptr

template<typename T>
char* BlobFromImage(cv::Mat& iImg, T& iBlob) {
    int channels = iImg.channels();
    int imgHeight = iImg.rows;
    int imgWidth = iImg.cols;

    for (int c = 0; c < channels; c++)
    {
        for (int h = 0; h < imgHeight; h++)
        {
            for (int w = 0; w < imgWidth; w++)
            {
                iBlob[c * imgWidth * imgHeight + h * imgWidth + w] = typename std::remove_pointer<T>::type(
                    (iImg.at<cv::Vec3b>(h, w)[c]) / 255.0f);
            }
        }
    }
    return RET_OK;
}


char* PreProcess(cv::Mat& iImg, std::vector<int> iImgSize, cv::Mat& oImg)
{
    if (iImg.channels() == 3)
    {
        oImg = iImg.clone();
        cv::cvtColor(oImg, oImg, cv::COLOR_BGR2RGB);
    }
    else
    {
        cv::cvtColor(iImg, oImg, cv::COLOR_GRAY2RGB);
    }
    
    float resizeScales;
    if (iImg.cols >= iImg.rows)
    {
        resizeScales = iImg.cols / (float)iImgSize.at(0);
        cv::resize(oImg, oImg, cv::Size(iImgSize.at(0), int(iImg.rows / resizeScales)));
    }
    else
    {
        resizeScales = iImg.rows / (float)iImgSize.at(0);
        cv::resize(oImg, oImg, cv::Size(int(iImg.cols / resizeScales), iImgSize.at(1)));
    }
    cv::Mat tempImg = cv::Mat::zeros(iImgSize.at(0), iImgSize.at(1), CV_8UC3);
    oImg.copyTo(tempImg(cv::Rect(0, 0, oImg.cols, oImg.rows)));
    oImg = tempImg;

    return RET_OK;
}

int main() {

    std::cout << "test onnx" << std::endl;
    // 设置模型路径和输入图像大小
    std::string onnx_model_path = "../models/best.onnx";
    std::vector<int> imgSize = { 640, 640 };
    // 设置参数
    Ort::Env env = Ort::Env(ORT_LOGGING_LEVEL_WARNING, "Yolo");
    Ort::SessionOptions sessionOption;
    OrtCUDAProviderOptions cudaOption;
    cudaOption.device_id = 0;
    sessionOption.AppendExecutionProvider_CUDA(cudaOption);
    sessionOption.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    sessionOption.SetIntraOpNumThreads(1);
    sessionOption.SetLogSeverityLevel(3);
    const char* modelPath = onnx_model_path.c_str();
    Ort::Session* session = new Ort::Session(env, modelPath, sessionOption); // 正式工程慎用 new
    // 获取输入输出节点
    std::vector<const char*> inputNodeNames;
    std::vector<const char*> outputNodeNames;
    Ort::AllocatorWithDefaultOptions allocator;
    size_t inputNodesNum = session->GetInputCount();
    for (size_t i = 0; i < inputNodesNum; i++)
    {
        Ort::AllocatedStringPtr input_node_name = session->GetInputNameAllocated(i, allocator);
        char* temp_buf = new char[50]; // 正式工程慎用 new
        strcpy(temp_buf, input_node_name.get());
        inputNodeNames.push_back(temp_buf);
    }
    size_t OutputNodesNum = session->GetOutputCount();
    for (size_t i = 0; i < OutputNodesNum; i++)
    {
        Ort::AllocatedStringPtr output_node_name = session->GetOutputNameAllocated(i, allocator);
        char* temp_buf = new char[10]; // 正式工程慎用 new
        strcpy(temp_buf, output_node_name.get());
        outputNodeNames.push_back(temp_buf);
    }
    Ort::RunOptions options = Ort::RunOptions{ nullptr };
    // 数据预处理
    cv::Mat iImg = cv::Mat(cv::Size(imgSize.at(0), imgSize.at(1)), CV_8UC3);
    cv::Mat processedImg;
    PreProcess(iImg, imgSize, processedImg);
    // 多次运行，确认在GPU上工作
    for (int k=0;k<2000;++k){
        float* blob = new float[iImg.total() * 3]; // 正式工程慎用 new
        BlobFromImage(processedImg, blob);
        std::vector<int64_t> YOLO_input_node_dims = { 1, 3, imgSize.at(0), imgSize.at(1) };
        Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
            Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU), blob, 3 * imgSize.at(0) * imgSize.at(1),
            YOLO_input_node_dims.data(), YOLO_input_node_dims.size());
        auto outputTensor = session->Run(options, inputNodeNames.data(), &input_tensor, 1, outputNodeNames.data(),
                outputNodeNames.size());
        // 解析输出张量
        Ort::TypeInfo typeInfo = outputTensor.front().GetTypeInfo();
        auto tensor_info = typeInfo.GetTensorTypeAndShapeInfo();
        std::vector<int64_t> outputNodeDims = tensor_info.GetShape();
        auto output = outputTensor.front().GetTensorMutableData<typename std::remove_pointer<float>::type>();
        delete[] blob;
        // 打印输出张量的维度
        std::cout << "k:" << k << " outputNodeDims:";
        for (auto i =0; i < outputNodeDims.size(); ++i) {
            std::cout << outputNodeDims[i] << " ";
        }
        std::cout << std::endl;
    }
    // 清理申请的内存，正式工程慎用这种方式
    for(auto p : inputNodeNames) {
        std::cout << "delete input name: " << p << std::endl;
        delete [] p;
    }
    for(auto p : outputNodeNames) {
        std::cout << "delete output name: " << p << std::endl;
        delete [] p;
    }
    delete session;
    
    return 0;
}
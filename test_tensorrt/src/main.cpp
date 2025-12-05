#include <iostream>
#include <vector>
#include <memory>
#include <string>
#include <fstream>
#include <algorithm>
#include <opencv2/opencv.hpp>
#include <NvInfer.h>
#include <NvOnnxParser.h>
#include <cuda_runtime_api.h>
#include <numeric>
#include <iomanip>

// 辅助函数：读取文件
std::vector<char> readFile(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        throw std::runtime_error("无法打开文件: " + filepath);
    }
    
    size_t size = file.tellg();
    file.seekg(0, std::ios::beg);
    
    std::vector<char> buffer(size);
    file.read(buffer.data(), size);
    file.close();
    
    return buffer;
}

// 辅助函数：写入文件
void writeFile(const std::string& filepath, const void* data, size_t size) {
    std::ofstream file(filepath, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("无法写入文件: " + filepath);
    }
    
    file.write(static_cast<const char*>(data), size);
    file.close();
}

// 日志记录器
class Logger : public nvinfer1::ILogger {
public:
    void log(Severity severity, const char* msg) noexcept override {
        if (severity <= Severity::kWARNING) {
            std::cout << "[TensorRT] " << msg << std::endl;
        }
    }
};

int main() {
    std::string engine_path = "../output/best.trt";

    // 读取引擎文件
    auto engine_data = readFile(engine_path);
    Logger logger_;
    
    // 创建runtime
    std::shared_ptr<nvinfer1::IRuntime> runtime_ = std::shared_ptr<nvinfer1::IRuntime>(
        nvinfer1::createInferRuntime(logger_),
        [](nvinfer1::IRuntime* p) { if (p) delete p; }
    );
    
    if (!runtime_) {
        std::cerr << "Failed to create TensorRT runtime" << std::endl;
        return false;
    }
    
    // 反序列化引擎
    std::shared_ptr<nvinfer1::ICudaEngine> engine_ = std::shared_ptr<nvinfer1::ICudaEngine>(
        runtime_->deserializeCudaEngine(engine_data.data(), engine_data.size()),
        [](nvinfer1::ICudaEngine* p) { if (p) delete p; }
    );
    
    if (!engine_) {
        std::cerr << "Failed to deserialize CUDA engine" << std::endl;
        return false;
    }
    
    // 创建执行上下文
    std::shared_ptr<nvinfer1::IExecutionContext> context_ = std::shared_ptr<nvinfer1::IExecutionContext>(
        engine_->createExecutionContext(),
        [](nvinfer1::IExecutionContext* p) { if (p) delete p; }
    );
    
    if (!context_) {
        std::cerr << "Failed to create execution context" << std::endl;
        return false;
    }
    
    // 模型信息
    int input_height_;
    int input_width_;
    int input_channels_;
    int input_batch_size_;
    int64_t input_size_;
    int output_size_;
    int output_dim_[4]; 
    // 获取绑定信息
    int input_binding_index_ = 0;
    int output_binding_index_ = 0;
    for (int i = 0; i < engine_->getNbIOTensors(); ++i) {
        auto name = engine_->getIOTensorName(i);
        if (engine_->getTensorIOMode(name) == nvinfer1::TensorIOMode::kINPUT) {
            input_binding_index_ = i;
            auto dims = engine_->getTensorShape(name);
            input_batch_size_ = dims.d[0];
            input_channels_ = dims.d[1];
            input_height_ = dims.d[2];
            input_width_ = dims.d[3];
            input_size_ = input_batch_size_ * input_channels_ * input_height_ * input_width_;
        } else {
            output_binding_index_ = i;
            auto dims = engine_->getTensorShape(name);
            output_dim_[0] = dims.d[0];  // batch
            output_dim_[1] = dims.d[1];  // num_detections
            output_dim_[2] = dims.d[2];  // 6: [x1, y1, x2, y2, conf, cls]
            output_size_ = output_dim_[0] * output_dim_[1] * output_dim_[2];
        }
    }
    std::cout << "模型输入尺寸: " << input_batch_size_ << "x" 
                << input_channels_ << "x" << input_height_ << "x" << input_width_ << std::endl;
    std::cout << "模型输出尺寸: " << output_dim_[0] << "x" 
                << output_dim_[1] << "x" << output_dim_[2] << std::endl;
    
    // 分配内存
    void* device_buffers_[2];  // [0]: input, [1]: output
    void* host_buffers_[2];    // [0]: input, [1]: output
    cudaStream_t stream_;
    // 分配设备内存
    cudaMalloc(&device_buffers_[0], input_size_ * sizeof(float));
    cudaMalloc(&device_buffers_[1], output_size_ * sizeof(float));
    // 分配主机内存（页锁定内存）
    cudaHostAlloc(&host_buffers_[0], input_size_ * sizeof(float), cudaHostAllocDefault);
    cudaHostAlloc(&host_buffers_[1], output_size_ * sizeof(float), cudaHostAllocDefault);
    std::cout << "内存分配成功" << std::endl;
    std::cout << "输入内存大小: " << input_size_ * sizeof(float) / 1024.0 / 1024.0 << " MB" << std::endl;
    std::cout << "输出内存大小: " << output_size_ * sizeof(float) / 1024.0 / 1024.0 << " MB" << std::endl;

    // 运行
    // 将数据复制到主机缓冲区
    cv::Mat preprocessed_image = cv::Mat::zeros(input_height_, input_width_, CV_32FC3);
    memcpy(host_buffers_[0], preprocessed_image.data, input_size_ * sizeof(float));
    
    // 主机到设备
    cudaMemcpyAsync(device_buffers_[0], host_buffers_[0], 
                    input_size_ * sizeof(float), 
                    cudaMemcpyHostToDevice, stream_);
    // 执行推理
    if (!context_->executeV2(device_buffers_)) {
        std::cerr << "推理执行失败" << std::endl;
        return 1;
    }
    // 设备到主机
    cudaMemcpyAsync(host_buffers_[1], device_buffers_[1], 
                    output_size_ * sizeof(float), 
                    cudaMemcpyDeviceToHost, stream_);
    cudaStreamSynchronize(stream_);
    std::cout << "output:";
    for(int k=0;k<output_size_;++k) {
        std::cout << *((float*)host_buffers_[1] + k) << ",";
        if (k>20) {
            break;
        }
    }
    std::cout << std::endl;

    // 释放主机内存
    if (host_buffers_[0]) {
        cudaFreeHost(host_buffers_[0]);
        host_buffers_[0] = nullptr;
    }
    if (host_buffers_[1]) {
        cudaFreeHost(host_buffers_[1]);
        host_buffers_[1] = nullptr;
    }
    
    // 释放设备内存
    if (device_buffers_[0]) {
        cudaFree(device_buffers_[0]);
        device_buffers_[0] = nullptr;
    }
    if (device_buffers_[1]) {
        cudaFree(device_buffers_[1]);
        device_buffers_[1] = nullptr;
    }
}
// simple_test.cpp - 最简测试
#include <torch/torch.h>
#include <torchvision/vision.h>
#include <torchvision/ops/nms.h>
#include <iostream>

int main() {
    try {
        std::cout << "TorchVision Minimal Test" << std::endl;
        
        // 测试1: 基础张量
        auto x = torch::tensor({1.0, 2.0, 3.0});
        std::cout << "Tensor created: " << x << std::endl;
        
        // 测试2: 图像操作函数
        auto img = torch::rand({3, 100, 100});
        // 使用插值函数
        auto resized = torch::nn::functional::interpolate(
            img.unsqueeze(0),
            torch::nn::functional::InterpolateFuncOptions()
                .scale_factor(std::vector<double>{0.5, 0.5})
                .mode(torch::kBilinear)
        );
        std::cout << "Image resize test: " 
                  << img.sizes() << " -> " 
                  << resized.sizes() << std::endl;
       
        // 测试torchvision中的nms
        // 创建测试数据
        auto boxes = torch::tensor({{4, 4, 14, 14}, {5, 5, 15, 15}}, torch::kFloat32);
        auto scores = torch::tensor({0.9, 0.95},  torch::kFloat32);
        // 调用 nms
        auto keep = vision::ops::nms(boxes, scores, 0.5);
        std::cout << "NMS result: " << keep << std::endl;	
        
	    std::cout << "\n✅ SUCCESS: TorchVision is working!" << std::endl;
        return 0;
        
    } catch (const c10::Error& e) {
        std::cerr << "PyTorch/TorchVision error: " << e.what() << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "General error: " << e.what() << std::endl;
        return 1;
    }
}

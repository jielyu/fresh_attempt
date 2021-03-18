#include <opencv2/opencv.hpp>
#include <iostream>
using namespace cv;

int main(int argc, char** argv) {
   cv::Mat a = cv::Mat::zeros(cv::Size(2,3), CV_64FC1);
   std::cout<<a<<std::endl;

    return 0;
}

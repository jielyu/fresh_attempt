#include <glog/logging.h>
#include <iostream>
#include <opencv2/opencv.hpp>
#include "xtensor/xarray.hpp"
#include "xtensor/xio.hpp"
#include "xtensor/xview.hpp"

int main(int argc, char *argv[])
{
    // 初始化 glog
    google::InitGoogleLogging(argv[0]);
    FLAGS_logtostderr = false;
    FLAGS_alsologtostderr = false;
    FLAGS_minloglevel = google::INFO;
    google::SetStderrLogging(google::INFO);
    std::cout << "当前minloglevel: " << FLAGS_minloglevel << ", info:" << google::INFO << ", warning:" << google::WARNING << ", error:" << google::ERROR << std::endl;

    // opencv
    cv::Mat a = cv::Mat::ones(3, 3, CV_64FC1);
    std::cout << "mat a=" << a << std::endl;

    // xtensor
    xt::xarray<double> arr1{{1.0, 2.0, 3.0},
                            {2.0, 5.0, 7.0},
                            {2.0, 5.0, 7.0}};
    xt::xarray<double> arr2{5.0, 6.0, 7.0};
    xt::xarray<double> res = xt::view(arr1, 1) + arr2;
    std::cout << res << std::endl;

    // 记录不同级别的日志
    LOG(INFO) << "这是一条 INFO 级别的日志";
    LOG(WARNING) << "这是一条 WARNING 级别的日志";
    LOG(ERROR) << "这是一条 ERROR 级别的日志";
    // LOG(FATAL) << "这是一条 FATAL 级别的日志，会终止程序";
    // CHECK(2 > 3) << "unexpect 2>3";

    // 条件日志
    int x = 10;
    LOG_IF(INFO, x > 5) << "x 大于 5";

    // 定期日志（每 10 次记录一次）
    for (int i = 0; i < 100; ++i)
    {
        LOG_EVERY_N(INFO, 10) << "每 10 次记录一次，这是第 " << google::COUNTER << " 次";
    }

    // 关闭 glog
    google::ShutdownGoogleLogging();
    return 0;
}
#include <iostream>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

// 接收任意类型的 NumPy 数组
py::tuple process_array(py::array arr)
{
    // 获取基本信息
    auto buf = arr.request();

    // 打印调试信息（可选）
    // std::cout << "Type: " << buf.format << "\n";
    // std::cout << "Dims: " << buf.ndim << "\n";
    // std::cout << "Shape: ";
    // for (ssize_t i = 0; i < buf.ndim; ++i) std::cout << buf.shape[i] << " ";
    // std::cout << "\n";

    // 返回形状（tuple）和总元素数
    py::tuple shape_tuple = py::tuple(buf.ndim);
    for (ssize_t i = 0; i < buf.ndim; ++i)
    {
        shape_tuple[i] = buf.shape[i];
    }

    return py::make_tuple(shape_tuple, buf.size);
}

// 接收 float64 类型的 1D 数组，并计算和
double sum_array(py::array_t<double> arr)
{
    // 自动检查类型和连续性（可选）
    py::buffer_info buf = arr.request();

    if (buf.ndim != 1)
    {
        throw std::runtime_error("Expected 1D array");
    }

    // 获取指针（安全：假设数组是连续的）
    auto ptr = static_cast<double *>(buf.ptr);
    double sum = 0.0;
    for (ssize_t i = 0; i < buf.shape[0]; ++i)
    {
        sum += ptr[i];
    }
    return sum;
}

// 修改数组（in-place）
void multiply_array(py::array_t<double> arr, double factor)
{
    py::buffer_info buf = arr.request();
    auto ptr = static_cast<double *>(buf.ptr);
    for (ssize_t i = 0; i < buf.size; ++i)
    {
        ptr[i] *= factor;
    }
}

py::array_t<double> create_array(ssize_t n)
{
    auto result = py::array_t<double>(n);
    auto buf = result.request();
    double *ptr = (double *)buf.ptr;
    for (ssize_t i = 0; i < n; i++)
    {
        ptr[i] = i + 9.5;
        // std::cout << "i=" << i << "; value=" << ptr[i] << std::endl;
    }
    return result;
}
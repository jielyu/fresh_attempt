#include <iostream>
#include <omp.h> // OpenMP 头文件
#include <pybind11/pybind11.h>

namespace py = pybind11;

void openmp_parallel()
{
    // 释放 GIL（关键！）
    py::gil_scoped_release release;

#pragma omp parallel for
    for (int i = 0; i < 8; ++i)
    {
        std::cout << "i:" << i << std::endl;
    }
}
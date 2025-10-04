#include <iostream>
#include <omp.h> // OpenMP 头文件

void openmp_parallel()
{
#pragma omp parallel for
    for (int i = 0; i < 8; ++i)
    {
        std::cout << "i:" << i << std::endl;
    }
}
#include <vector>

// 传入list
double sum_list(const std::vector<double> &numbers)
{
    double total = 0.0;
    for (double x : numbers)
    {
        total += x;
    }
    return total;
}

// 返回list
std::vector<int> range(int start, int end)
{
    std::vector<int> result;
    for (int i = start; i < end; ++i)
    {
        result.push_back(i);
    }
    return result;
}
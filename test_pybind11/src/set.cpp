#include <set>
#include "set_cast.h"
// 现在可以绑定接收 std::set 的函数
std::string describe_set(const std::set<int> &s)
{
    std::string result = "{";
    for (auto it = s.begin(); it != s.end(); ++it)
    {
        if (it != s.begin())
            result += ", ";
        result += std::to_string(*it);
    }
    result += "}";
    return result;
}
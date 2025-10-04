#include <map>
#include <string>
#include <unordered_map>

int total_scores(const std::map<std::string, int> &scores)
{
    int total = 0;
    for (const auto &[name, score] : scores)
    {
        total += score;
    }
    return total;
}

double average_scores(const std::unordered_map<std::string, double> &scores)
{
    if (scores.empty())
        return 0.0;
    double sum = 0.0;
    for (const auto &kv : scores)
    {
        sum += kv.second;
    }
    return sum / scores.size();
}

// 返回dict
std::map<std::string, int> create_score_map()
{
    return {{"Alice", 100}, {"Bob", 90}};
}
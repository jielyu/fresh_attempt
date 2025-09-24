#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11_json/pybind11_json.hpp> // 关键：启用 json <-> Python 转换
#include <nlohmann/json.hpp>

namespace py = pybind11;
using json = nlohmann::json;

json create_config()
{
    return {
        {"name", "Alice"},
        {"age", 30},
        {"active", true},
        {"scores", {95, 87, 92}}};
}

void print_json(const json &j)
{
    std::cout << j.dump(2) << std::endl;
}

int multiply(int a, int b)
{
    return a * b;
}

PYBIND11_MODULE(example, m)
{
    m.doc() = "Example pybind11 module built with Conan";
    m.def("multiply", &multiply, "Multiply two integers");
    // 自动转换：C++ json ↔ Python dict/list
    m.def("create_config", &create_config, "Return a JSON object as Python dict");
    m.def("print_json", &print_json, "Print a JSON object from Python dict");
}
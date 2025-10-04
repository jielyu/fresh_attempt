#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>                  // 必须在导出模块的文件中包含，否则无法自动进行类型转换
#include "pybind11_json/pybind11_json.hpp" // 关键：启用 json <-> Python 转换
#include <nlohmann/json.hpp>
#include <pybind11/numpy.h>

namespace py = pybind11;

// 基本测试函数
int multiply(int a, int b)
{
    return a * b;
}

// list操作函数
double sum_list(const std::vector<double> &numbers);
std::vector<int> range(int start, int end);

// dict操作函数
int total_scores(const std::map<std::string, int> &scores);
double average_scores(const std::unordered_map<std::string, double> &scores);
std::map<std::string, int> create_score_map();

// set
std::string describe_set(const std::set<int> &s);

// json操作函数
using json = nlohmann::json;
json create_config();
void print_json(const json &j);

// class
#include "class.h"

// numpy
py::tuple process_array(py::array arr);
double sum_array(py::array_t<double> arr);
void multiply_array(py::array_t<double> arr, double factor);
py::array_t<double> create_array(ssize_t n);

// openmp
void openmp_parallel();

PYBIND11_MODULE(example, m)
{
    m.doc() = "Example pybind11 module built with Conan";
    m.def("multiply", &multiply, "Multiply two integers");
    // list/tuple
    m.def("sum_list", &sum_list, "Sum all numbers in a list");
    m.def("range", &range);
    // dict
    m.def("total_scores", &total_scores, "Sum all values in dict");
    m.def("average_scores", &average_scores);
    m.def("create_score_map", &create_score_map);
    // set
    m.def("describe_set", &describe_set);
    // 自动转换：C++ json ↔ Python dict/list
    m.def("create_config", &create_config, "Return a JSON object as Python dict");
    m.def("print_json", &print_json, "Print a JSON object from Python dict");
    // class
    py::class_<Pet>(m, "Pet", py::dynamic_attr())
        .def(py::init<const std::string &>())        // 构造函数
        .def_readwrite("nick_name", &Pet::nick_name) // 可读写
        .def_readonly("age", &Pet::age)              // 只读
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName)
        .def("__repr__", [](const Pet &p)
             { return "<Pet name='" + p.getName() + "'>"; });
    // numpy
    m.def("process_array", &process_array, "Process any NumPy array");
    m.def("sum_array", &sum_array, "Sum a 1D float64 NumPy array");
    m.def("multiply_array", &multiply_array, "Multiply array in-place by a factor");
    m.def("create_array", &create_array, "Create numpy array");
    // openmp
    m.def("openmp_parallel", &openmp_parallel, "check openmp parallel");
}
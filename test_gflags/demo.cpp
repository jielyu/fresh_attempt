#include <iostream>
#include <gflags/gflags.h>

DEFINE_int32(arg1, 0, "arg1");
DEFINE_bool(arg2, true, "arg2");

int main(int argc, char ** argv) {
    google::ParseCommandLineFlags(&argc, &argv, true);
    std::cout << FLAGS_arg1 << ", " << FLAGS_arg2 << std::endl;
    return 0;
}

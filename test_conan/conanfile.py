import os
from conan import ConanFile
from conan.tools.cmake import CMake
from conan.tools.cmake import cmake_layout


class ShapeAlignmentConan(ConanFile):
    name = "test_conan"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires("glog/0.7.1")
        self.requires("opencv/4.10.0")
        self.requires("xtensor/0.25.0")

    def build_requirements(self):
        self.tool_requires("cmake/3.27.9")

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.run("./test_conan")

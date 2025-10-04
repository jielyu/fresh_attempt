from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class PyBind11Example(ConanFile):
    name = "example"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("pybind11/3.0.1")
        # self.requires("pybind11/2.10.4")
        # self.requires("pybind11_json/0.2.13")

    def build_requirements(self):
        self.tool_requires("cmake/3.27.9")

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

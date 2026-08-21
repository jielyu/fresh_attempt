from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout


class ThorvgBooleanDemo(ConanFile):
    """ThorVG 矢量路径布尔运算演示工程。

    依赖说明：
      - thorvg/0.15.16 : 矢量渲染引擎，负责把布尔运算结果光栅化到像素缓冲
      - clipper2/1.3.0 : 多边形布尔运算库，负责 Union / Difference / Intersect
      - libpng         : ThorVG 0.15 没有 PNG saver，需自行用 libpng 编码 PNG
    """

    name = "thorvg_boolean_demo"
    version = "0.1.0"
    package_type = "application"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    requires = [
        "thorvg/0.15.16",
        "clipper2/1.3.0",
        "libpng/[>=1.6.43 <2]",
    ]

    default_options = {
        # 最小化 thorvg 构建：仅 sw 引擎，不编译 loader / saver / CAPI 绑定 / lottie 表达式
        "thorvg/*:with_engines": "sw",
        "thorvg/*:with_loaders": False,
        "thorvg/*:with_savers": False,
        "thorvg/*:with_bindings": False,
        "thorvg/*:with_extra": False,
    }

    def layout(self):
        cmake_layout(self)

    def generate(self):
        CMakeToolchain(self).generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

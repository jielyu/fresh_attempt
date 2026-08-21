// main.cpp
//
// ThorVG + Clipper2 矢量路径布尔运算案例
//
// 流程：
//   1. 三个圆形图形先用 Clipper2 离散化为多边形（圆弧 -> 线段逼近，128 段）
//   2. Clipper2 执行相加(Union) / 相减(Difference) / 交集(Intersect)
//   3. 布尔结果多边形路径交给 ThorVG 光栅化到像素缓冲
//   4. 用 libpng 将像素缓冲编码为 PNG
//
// 说明：ThorVG 0.15 没有 PNG saver（只支持 tvg/gif），故自行用 libpng 编码。
//
// 构建/运行：见 README.md

#include <thorvg.h>
#include <clipper2/clipper.h>
#include <png.h>

#include <cmath>
#include <csetjmp>
#include <cstdint>
#include <cstdio>
#include <filesystem>
#include <memory>
#include <string>
#include <vector>

using namespace Clipper2Lib;

namespace {

constexpr uint32_t kWidth  = 320;
constexpr uint32_t kHeight = 320;

constexpr double kPi = 3.14159265358979323846;

// 把圆离散化为闭合多边形（默认 128 段，Clipper2 隐式闭合首尾）
PathD makeCircle(double cx, double cy, double r, int segments = 128)
{
    PathD path;
    path.reserve(segments);
    for (int i = 0; i < segments; ++i) {
        const double a = 2.0 * kPi * i / segments;
        path.emplace_back(cx + r * std::cos(a), cy + r * std::sin(a));
    }
    return path;
}

// 把 Clipper2 的多边形结果转成 ThorVG 的 Shape 路径
std::unique_ptr<tvg::Shape> toThorvgShape(const PathsD& paths)
{
    auto shape = tvg::Shape::gen();
    for (const auto& path : paths) {
        if (path.size() < 3) continue;
        shape->moveTo(static_cast<float>(path[0].x), static_cast<float>(path[0].y));
        for (size_t i = 1; i < path.size(); ++i) {
            shape->lineTo(static_cast<float>(path[i].x), static_cast<float>(path[i].y));
        }
        shape->close();
    }
    // EvenOdd 不依赖环的绕向，能正确渲染带孔(内环)的多边形
    shape->fill(tvg::FillRule::EvenOdd);
    return shape;
}

// 把 ARGB8888S 像素缓冲编码为 PNG
bool writePng(const std::string& filename, const uint32_t* buffer, uint32_t w, uint32_t h)
{
    // ARGB8888S 像素布局为 0xAARRGGBB，转换成 PNG 的 RGBA 字节序
    std::vector<png_byte> rgba(static_cast<size_t>(w) * h * 4);
    for (uint32_t i = 0; i < w * h; ++i) {
        const uint32_t v = buffer[i];
        rgba[i * 4 + 0] = static_cast<png_byte>((v >> 16) & 0xff);  // R
        rgba[i * 4 + 1] = static_cast<png_byte>((v >> 8) & 0xff);   // G
        rgba[i * 4 + 2] = static_cast<png_byte>(v & 0xff);          // B
        rgba[i * 4 + 3] = static_cast<png_byte>((v >> 24) & 0xff);  // A
    }

    FILE* fp = std::fopen(filename.c_str(), "wb");
    if (!fp) return false;

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, nullptr, nullptr, nullptr);
    if (!png) {
        std::fclose(fp);
        return false;
    }
    png_infop info = png_create_info_struct(png);
    if (!info || setjmp(png_jmpbuf(png))) {
        png_destroy_write_struct(&png, &info);
        std::fclose(fp);
        return false;
    }

    png_init_io(png, fp);
    png_set_IHDR(png, info, w, h, 8, PNG_COLOR_TYPE_RGBA,
                 PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_DEFAULT, PNG_FILTER_TYPE_DEFAULT);
    png_write_info(png, info);

    std::vector<png_bytep> rows(h);
    for (uint32_t y = 0; y < h; ++y)
        rows[y] = rgba.data() + static_cast<size_t>(y) * w * 4;
    png_write_image(png, rows.data());
    png_write_end(png, info);

    png_destroy_write_struct(&png, &info);
    std::fclose(fp);
    return true;
}

// 渲染布尔结果到固定画布并保存 PNG
bool renderToPng(const std::string& filename, const PathsD& paths)
{
    // 透明背景
    std::vector<uint32_t> buffer(kWidth * kHeight, 0x00000000u);

    auto canvas = tvg::SwCanvas::gen();
    if (canvas->target(buffer.data(), kWidth, kWidth, kHeight, tvg::SwCanvas::ARGB8888S) != tvg::Result::Success)
        return false;

    // 布尔结果形状，红色填充，背景透明
    auto shape = toThorvgShape(paths);
    shape->fill(235, 90, 90, 255);
    if (canvas->push(std::move(shape)) != tvg::Result::Success) return false;

    if (canvas->draw() != tvg::Result::Success) return false;
    if (canvas->sync() != tvg::Result::Success) return false;

    if (!writePng(filename, buffer.data(), kWidth, kHeight)) {
        std::fprintf(stderr, "writePng(%s) 失败\n", filename.c_str());
        return false;
    }
    return true;
}

void dumpResult(const char* op, const PathsD& paths)
{
    std::printf("[%s] 环数=%zu", op, paths.size());
    for (size_t i = 0; i < paths.size(); ++i) {
        std::printf("  环[%zu]=%zu 点", i, paths[i].size());
    }
    std::printf("\n");
}

}  // namespace

int main()
{
    if (tvg::Initializer::init(tvg::CanvasEngine::Sw, 0) != tvg::Result::Success) {
        std::fprintf(stderr, "ThorVG 初始化失败\n");
        return 1;
    }

    // 输出目录
    std::filesystem::create_directories("output");

    // 三个圆，等腰三角形排列，两两相交且中心有公共交集
    const PathsD circleA{makeCircle(150.0, 130.0, 80.0)};
    const PathsD circleB{makeCircle(100.0, 220.0, 80.0)};
    const PathsD circleC{makeCircle(200.0, 220.0, 80.0)};

    constexpr FillRule kFillRule = FillRule::NonZero;
    constexpr int kPrecision = 2;  // 布尔运算保留的小数位数

    // 1) 相加：A ∪ B ∪ C
    auto unionPaths = Union(circleA, circleB, kFillRule, kPrecision);
    unionPaths = Union(unionPaths, circleC, kFillRule, kPrecision);
    dumpResult("Union", unionPaths);
    renderToPng("output/union.png", unionPaths);

    // 2) 相减：A − B − C
    auto diffPaths = Difference(circleA, circleB, kFillRule, kPrecision);
    diffPaths = Difference(diffPaths, circleC, kFillRule, kPrecision);
    dumpResult("Subtract", diffPaths);
    renderToPng("output/subtract.png", diffPaths);

    // 3) 交集：A ∩ B ∩ C
    auto interPaths = Intersect(circleA, circleB, kFillRule, kPrecision);
    interPaths = Intersect(interPaths, circleC, kFillRule, kPrecision);
    dumpResult("Intersect", interPaths);
    renderToPng("output/intersect.png", interPaths);

    tvg::Initializer::term(tvg::CanvasEngine::Sw);
    std::printf("完成：已生成 output/union.png / output/subtract.png / output/intersect.png\n");
    return 0;
}

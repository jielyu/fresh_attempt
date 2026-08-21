# ThorVG 矢量路径布尔运算案例

使用 `thorvg/0.15.16` 与 `clipper2` 实现三个矢量图形（圆形）的**相加、相减、交集**，
结果由 ThorVG 光栅化并导出为 PNG。依赖使用 **conan2** 管理。

## 背景：为什么需要 Clipper2

ThorVG 0.15 **没有矢量路径级的布尔运算 API**：
- `Shape` 类没有 `union`/`subtract`/`intersect` 方法，只提供路径绘制、填充、描边。
- 也没有 PNG saver（`with_savers` 只支持 `tvg`、`gif`）。

因此本案例的分工是：

```
圆(弧形)
  │  Clipper2：先离散化为 128 段多边形（Clipper2 只处理多边形）
  ▼
多边形 ──Clipper2 布尔运算(Union/Difference/Intersect)──▶ 结果多边形
  │  ThorVG：将结果路径光栅化到像素缓冲
  ▼
像素缓冲 ──libpng：编码为 PNG──▶ union.png / subtract.png / intersect.png
```

> 注意：布尔运算的结果是**多边形**（圆弧的离散化逼近），不是真正的曲线路径。
> 这也是所有多边形布尔库（Clipper2、GDAL/GEOS、Qt 等）处理弧形的通用做法。

## 项目结构

```
├── conanfile.py      # conan2 依赖清单：thorvg、clipper2、libpng
├── CMakeLists.txt    # CMake 构建，CMakeDeps 集成三个依赖
├── src/
│   └── main.cpp      # 示例代码：三圆布尔运算 + ThorVG 渲染 + libpng 编码
├── build/            # conan/cmake 构建产物
└── output/           # 运行产物（三张 PNG）
```

## 构建与运行

```bash
# 1. 安装依赖（缺失的包会自动从源码构建）
conan install . --build=missing

# 2. 构建
conan build .

# 3. 运行
./build/Release/path_boolean
```

运行后在 `output/` 目录生成三张 PNG：

| 文件 | 运算 | 含义 |
|---|---|---|
| `union.png` | 相加 | A ∪ B ∪ C |
| `subtract.png` | 相减 | A − B − C |
| `intersect.png` | 交集 | A ∩ B ∩ C |

## 示例中的三个圆

三个半径 80 的圆，等腰三角形排列，两两相交且有公共交集：

| 圆 | 圆心 |
|---|---|
| A | (150, 130) |
| B | (100, 220) |
| C | (200, 220) |

## 关键实现点

- **圆的离散化**：`makeCircle()` 将圆采样为 128 段闭合多边形（见 `src/main.cpp`）。
- **布尔运算**：`Clipper2Lib::Union / Difference / Intersect`，精度保留 2 位小数。
- **带孔结果**：ThorVG 渲染使用 `FillRule::EvenOdd`，不依赖环的绕向，能正确显示内孔。
- **PNG 编码**：ThorVG 渲染到 `SwCanvas` 的 `ARGB8888S` 缓冲后，用 libpng 手动编码为 RGBA PNG。
- **thorvg 构建选项**已最小化：仅 `sw` 引擎，不编译 loader/saver/绑定/lottie 表达式（可显著加快构建）。

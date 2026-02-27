// src/lib.rs
// （可选）也可以在 Cargo.toml 中配置 crate-type，二选一
// #[crate_type = "staticlib"]

// 禁止 Rust 混淆函数名，确保 C 能找到该函数
#[unsafe(no_mangle)]
// 声明函数遵循 C 调用规范
pub extern "C" fn rust_add(a: i32, b: i32) -> i32 {
    a + b
}

// 定义 C 兼容的结构体（#[repr(C)] 保证内存布局和 C 一致）
#[repr(C)]
#[derive(Debug)]
pub struct RustPoint {
    pub x: f64,
    pub y: f64,
}

#[unsafe(no_mangle)]
pub extern "C" fn rust_point_distance(p1: RustPoint, p2: RustPoint) -> f64 {
    ((p1.x - p2.x).powi(2) + (p1.y - p2.y).powi(2)).sqrt()
}

// 可选：测试函数（仅 Rust 内部可用）
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rust_add() {
        assert_eq!(rust_add(2, 3), 5);
    }
}
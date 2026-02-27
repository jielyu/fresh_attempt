use std::process::Command;

fn main() {
    // 每次编译时自动生成头文件
    Command::new("cbindgen")
        .arg("--config")
        .arg("cbindgen.toml")
        .arg(".")
        .arg("-o")
        .arg("my_static_lib.h")
        .status()
        .expect("Failed to generate header file with cbindgen");

    // 告诉 Cargo 静态库的输出路径
    // println!("cargo:rustc-link-lib=static=my_static_lib");
    // println!("cargo:rustc-link-search=native=target/release");
}
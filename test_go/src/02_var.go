package main

import "fmt"

func main() {
	// 基本类型
	var str string = "hello"
	var i int = 1024
	var b bool = true
	fmt.Println(str, i, b)

	// 自动推导的声明方式
	var str2 = "world"
	fmt.Println(str2)

	// 省略var的声明方式
	str3 := "hello world"
	fmt.Println(str3)

	// 指针
	var cont int = 3
	var p = &cont
	fmt.Println(p, *p)
}

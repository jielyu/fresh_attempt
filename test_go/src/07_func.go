package main

import "fmt"

// 一般函数
func general(a int, b float32) int {
	fmt.Println(a, b)
	return 0
}

// 参数为指针的函数
func func_ptr(a *int) {
	fmt.Printf("before a=%d\n", *a)
	*a = 0
}

// 返回多个参数的函数
func func_mul_ret() (a int, b float32) {
	a = 12
	b = 3.14
	return
}

// 复合类型的方法
type Point struct {
	x int
	y int
}

func (p *Point) set_xy(x int, y int) {
	p.x = x
	p.y = y
}

func main() {
	fmt.Println(general(12, 3.14))
	a := 12
	func_ptr(&a)
	fmt.Printf("after a=%d\n", a)

	ret_a, ret_b := func_mul_ret()
	fmt.Printf("mul ret: a=%v, b=%v\n", ret_a, ret_b)

	var p Point
	p.set_xy(1, 1)
	fmt.Printf("p.x=%v, p.y=%v\n", p.x, p.y)
}

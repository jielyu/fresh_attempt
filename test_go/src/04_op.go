package main

import "fmt"

func main() {
	// 基本运算符与C/C++一致
	var a = 1024
	var b = 512
	fmt.Printf("%v+%v=%v\n", a, b, a+b)
	fmt.Printf("%v-%v=%v\n", a, b, a-b)
	fmt.Printf("%v*%v=%v\n", a, b, a*b)
	fmt.Printf("%v/%v=%v\n", a, b, a/b)
	fmt.Printf("%v%%%v=%v\n", a, b, a%b)
}

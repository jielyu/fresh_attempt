package main

import "fmt"

func main() {
	var m = make(map[int]int)
	m[1] = 1
	m[2] = 2
	fmt.Println(m)

	// 检查key是否命中
	_, ok := m[3]
	fmt.Println(ok)
}

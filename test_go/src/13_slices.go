package main

import "fmt"

/* 测试切片修改内容的影响

1. 切片之间是否会相互影响取决于是否共享底层数组

2. make创建切片时会自动创建一个匿名的底层数组

*/

func main() {
	// 切片共享底层数组的情况
	arr := [5]int{0, 1, 2, 3, 4}
	s1 := arr[0:3]
	s2 := arr[2:5]
	s1[2] = 10
	for _, v := range s1 {
		fmt.Printf("%v ", v)
	}
	fmt.Println()
	for _, v := range s2 {
		fmt.Printf("%v ", v)
	}
	fmt.Println()

	// 测试copy复制切片的作用
	s3 := make([]int, 2)
	copy(s3, s2)
	//s3 := s2
	s3[0] = 20
	for _, v := range s1 {
		fmt.Printf("%v ", v)
	}
	fmt.Println()
	for _, v := range s2 {
		fmt.Printf("%v ", v)
	}
	fmt.Println()
	for _, v := range s3 {
		fmt.Printf("%v ", v)
	}
	fmt.Println()

}

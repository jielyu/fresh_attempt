package main

import "fmt"

func main() {
	// 一般
	var sum = 0
	for i := 0; i <= 100; i++ {
		sum += i
	}
	fmt.Printf("sum=%d\n", sum)

	// range
	l1 := []int{1, 2, 3, 4, 5}
	var sum1 = 0
	for _, val := range l1 {
		sum1 += val
	}
	fmt.Printf("sum1=%d\n", sum1)
}

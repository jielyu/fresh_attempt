package main

import "fmt"

func main() {

	var arr = []int{1, 2, 3}
	arr[2] = 10
	fmt.Printf("%v, %v, %v\n", arr, arr[0], arr[2])

	var arr2 = []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	fmt.Println(arr2[2:9])
	fmt.Println(arr2[:5])
	fmt.Println(arr2[5:])
}

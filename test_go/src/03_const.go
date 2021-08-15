package main

import "fmt"

const (
	SUCC = iota
	WARNING
	TEST = "hello"
	INFO
	TEST_IOTA = iota
)

func main() {
	const i int = 1024
	fmt.Println(i)
	fmt.Println(SUCC, WARNING, TEST, INFO, TEST_IOTA)
}

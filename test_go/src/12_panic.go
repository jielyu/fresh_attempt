package main

import "fmt"

func f() {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("exception:", err)
		}
	}()
	panic("failed to call function")
}

func main() {
	f()
}

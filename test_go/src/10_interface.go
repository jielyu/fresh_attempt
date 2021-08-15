package main

import "fmt"

type Phone interface {
	call()
}

type IPhone struct{}

func (p IPhone) call() {
	fmt.Println("iphone")
}

type Android struct{}

func (p Android) call() {
	fmt.Println("android")
}

func main() {
	var p Phone
	p = new(IPhone)
	p.call()

	p = new(Android)
	p.call()
}

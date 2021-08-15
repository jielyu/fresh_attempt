package main

import (
	"fmt"
	"time"
)

func say(s string, c chan int) {
	for i := 0; i < 5; i++ {
		time.Sleep(100 * time.Millisecond)
		fmt.Println(s)
	}
	c <- 3
}

func main() {
	c := make(chan int, 2)
	go say("world", c)
	say("hello", c)
	fmt.Println(<-c)
	fmt.Println(<-c)
}

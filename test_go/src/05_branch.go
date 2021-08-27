package main

import "fmt"

func main() {
	// if 分支
	//var b = true
	if b := true; b {
		fmt.Println("true branch")
	} else {
		fmt.Println("false branch")
	}

	// switch 每个case自带break语句
	var i = 0
	switch i {
	case 0:
		fmt.Println("case 0")
	case 1:
		fmt.Println("case 1")
	case 2:
		fmt.Println("case 2")
	default:
		fmt.Println("case default")
	}

	// select会随机挑选一个运行

}

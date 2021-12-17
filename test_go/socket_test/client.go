package main

import (
	"fmt"
	"net"
	"os"
)

/// 用于检查错误信息，如果发生错误则退出
func checkError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %s", err)
		os.Exit(1)
	}
}

func main() {
	addr := "127.0.0.1:50051"
	// 解析TCP地址
	tcpAddr, err := net.ResolveTCPAddr("tcp4", addr)
	checkError(err)
	// 创建连接
	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	checkError(err)
	defer conn.Close()
	fmt.Printf("connect to %s succ\n", addr)

	// 创建缓冲区
	buf := make([]byte, 1024)
	var words = ""
	for {
		// 从命令行读取输入信息
		fmt.Printf(">:")
		fmt.Scan(&words)
		conn.Write([]byte(words))
		fmt.Printf("send data succ\n")

		// 从服务器读取输入信息
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Printf("recv data from %s finished\n", conn.RemoteAddr().String())
			break
		}
		fmt.Printf("recv:%s\n", string(buf[:n]))
	}
}

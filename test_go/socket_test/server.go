package main

import (
	"fmt"
	"net"
	"os"
	"strings"
)

/// 检查错误信息，发生错误则直接报错
func checkError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "error: %s", err)
		os.Exit(1)
	}
}

/// 具体处理请求的逻辑，使用goroutine调用
func handleConn(conn net.Conn) {
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Printf("recv data from %s finished\n", conn.RemoteAddr().String())
			return
		}
		fmt.Printf("recv:%s\n", string(buf[:n]))
		conn.Write([]byte(strings.ToUpper(string(buf[:n]))))
	}
}

func main() {
	addr := "127.0.0.1:50051"
	// 监听端口
	socket, err := net.Listen("tcp", addr)
	checkError(err)
	defer socket.Close()
	fmt.Printf("start listening on %s\n", addr)
	for {
		// 接收请求
		conn, err := socket.Accept()
		if err != nil {
			continue
		}
		fmt.Printf("create connect succ to: %s\n", conn.RemoteAddr().String())
		// 处理请求
		go handleConn(conn)
	}
}

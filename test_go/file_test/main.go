package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	//"strings"
)

func ReadAll(p string) string {
	f, err := os.Open(p)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	cont, err := ioutil.ReadAll(f)
	if err != nil {
		panic(err)
	}
	return string(cont)
}

func ReadAllDirect(p string) string {
	cont, err := ioutil.ReadFile(p)
	if err != nil {
		panic(err)
	}
	return string(cont)
}

func ReadFileWithBytes(p string) string {
	f, err := os.Open(p)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	reader := bufio.NewReader(f)
	chunks := make([]byte, 0)
	buff := make([]byte, 1024)
	for {
		n, err := reader.Read(buff)
		if err != nil && err != io.EOF {
			panic(err)
		}
		if n == 0 {
			break
		}
		chunks = append(chunks, buff[:n]...)
	}
	return string(chunks)
}

func ReadFileWithLine(p string) string {
	f, err := os.OpenFile(p, os.O_RDWR, 0666)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	ret := ""
	buff := bufio.NewReader(f)
	for {
		line, err := buff.ReadString('\n')
		//line = strings.TrimSpace(line)
		if err != nil {
			if err == io.EOF {
				break
			} else {
				panic(err)
			}
		}
		ret += line
	}
	return ret
}

func WriteAll(p string, cont string) {
	err := ioutil.WriteFile(p, []byte(cont), 0644)
	if err != nil {
		panic(err)
	}
}

func CheckFileExist(p string) bool {
	if _, err := os.Stat(p); os.IsNotExist(err) {
		return false
	}
	return true
}

func WriteAppend(p string, cont string) {
	var f *os.File
	var err error
	if CheckFileExist(p) {
		f, err = os.OpenFile(p, os.O_APPEND|os.O_RDWR, 0666)
	} else {
		f, err = os.Create(p)
	}
	defer f.Close()
	if err != nil {
		panic(err)
	}
	_, err = io.WriteString(f, cont)
	//_, err = f.WriteString(cont)  // 直接操作也可以
	if err != nil {
		panic(err)
	}
}

func main() {
	fmt.Println("file operations testcase")
	p := "./file_test.txt"

	WriteAll(p, "write file succ\n")
	WriteAppend(p, "append text\n")

	fmt.Println("ReadAll:", ReadAll(p))
	fmt.Println("ReadAllDirect:", ReadAllDirect(p))
	fmt.Println("ReadFileWithBytes:", ReadFileWithBytes(p))
	fmt.Println("ReadFileWithLine:", ReadFileWithLine(p))

}

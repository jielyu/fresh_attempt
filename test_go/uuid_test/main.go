package main

import "github.com/google/uuid"
import "fmt"

func main() {
	uuid := uuid.New()
	fmt.Println(uuid.String())
}

package main

import (
	"fmt"
	"reflect"
	"register_class/src/register_class"
)

type TestOp struct {
}

func (test_op *TestOp) Process() int {
	fmt.Println("TestOp process")
	return 0
}

func init() {
	register_class.RegisterClass("TestOp", func() register_class.BaseClass {
		return new(TestOp)
	})
}

type TestOp2 struct{}

func (test_op *TestOp2) Process() int {
	fmt.Println("TestOp2 process")
	return 0
}

func init() {
	register_class.RegisterClass("TestOp2", func() register_class.BaseClass {
		return new(TestOp2)
	})
}

// 测试调用基类函数
type BaseTest struct{}

func (b *BaseTest) hello() int {
	fmt.Println("BaseTest")
	return 0
}

type ChildTest struct {
	BaseTest
}

func (c *ChildTest) hello() int {
	c.BaseTest.hello()
	fmt.Println("ChildTest")
	return 0
}

func main() {
	fmt.Println("register_class")
	// 创建第一个类型的实例
	op := register_class.CreateInstance("TestOp")
	op.Process()
	// 创建第二个类型的实例
	op2 := register_class.CreateInstance("TestOp2")
	op2.Process()
	// 创建一个不存在类型的实例
	not_exist_op := register_class.CreateInstance("Hello")
	if not_exist_op != nil {
		not_exist_op.Process()
	}
	// 测试任意值类型的词典
	data := make(map[string]interface{})
	data["hello"] = 1
	data["world"] = "hello"
	type NewTestType struct{}
	data["newtype"] = new(NewTestType)
	data["test"] = new(interface{})
	data["test"] = 1
	fmt.Println(data)
	fmt.Println(reflect.TypeOf(data["hello"]))
	fmt.Println(reflect.TypeOf(data["world"]))
	fmt.Println(reflect.TypeOf(data["newtype"]))
	fmt.Println(reflect.TypeOf(data["test"]))

	// 测试子类调用基类函数
	b := new(ChildTest)
	b.hello()
}

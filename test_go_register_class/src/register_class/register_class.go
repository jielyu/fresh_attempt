package register_class

import "fmt"

type BaseClass interface {
	Process() int
}

var (
	factory_registry = make(map[string]func() BaseClass)
)

func RegisterClass(name string, fac_func func() BaseClass) {
	factory_registry[name] = fac_func
}

func CreateInstance(name string) BaseClass {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println(err)
		}
	}()
	if f, ok := factory_registry[name]; ok {
		return f()
	} else {
		info_str := fmt.Sprintf("not found Class[%s]", name)
		panic(info_str)
	}
}

# encoding: utf-8

import example


def main():

    p = example.Pet("Fido")
    print(p.getName())  # 输出: Fido
    p.setName("Buddy")
    print(p)
    # 动态增加属性
    p.dyn_name = "dynamic"
    print("dyn_name:", p.dyn_name)
    #
    p.nick_name = "dahuang"
    print(f"nick_name: {p.nick_name}, age: {p.age}")
    # p.age = 10 // 会报错，只能读不能写


if __name__ == "__main__":
    main()

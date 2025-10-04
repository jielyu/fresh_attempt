# encoding: utf-8

import example


def test_list_args():
    # 全是double
    print(example.sum_list([1.0, 2.0, 3.5]))  # 6.5
    # int和double
    print(example.sum_list([1, 2, 3.5]))  # 6.5
    # 空数组
    print(example.sum_list([]))  # 0.0
    # 全是int的tuple
    print(example.sum_list((1, 2, 3)))
    # 会报错，最后一个不是数值类型
    # print(example.sum_list((1, 2, "3")))


def test_return_list():
    print(example.range(1, 5))


def main():

    test_list_args()
    test_return_list()


if __name__ == "__main__":
    main()

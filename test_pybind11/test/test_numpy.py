# encoding: utf-8

import numpy as np
import example


def main():
    # 示例 1: 任意数组
    arr1 = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)
    shape, size = example.process_array(arr1)
    print("Shape:", shape)  # (2, 3)
    print("Size:", size)  # 6

    # 示例 2: 求和（必须是 float64 1D）
    arr2 = np.array([1.0, 2.0, 3.0, 4.0])
    total = example.sum_array(arr2)
    print("Sum:", total)  # 10.0

    # 示例 3: 原地修改
    arr3 = np.array([1.0, 2.0, 3.0])
    example.multiply_array(arr3, 2.0)
    print("Modified:", arr3)  # [2. 4. 6.]

    #
    np_arr = example.create_array(10)
    print("create array:", np_arr)


if __name__ == "__main__":
    main()

# encoding: utf-8

import example


def test_dict_args():
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("total_scores:", example.total_scores(scores))  # 输出: 274
    print("average_scores:", example.average_scores(scores))


def test_return_dict():
    print(example.create_score_map())


def main():
    test_dict_args()
    test_return_dict()


if __name__ == "__main__":
    main()

# encoding: utf-8

import example


def test_multiply():
    print(f"multiply(6*7): {example.multiply(6, 7)}")


def test_create_config():
    print(f"create_config: {example.create_config()}")


def test_print_json():
    config = {"a": 1, "b": "hello"}
    example.print_json(config)


def main():
    test_multiply()
    test_create_config()
    test_print_json()


if __name__ == "__main__":
    main()

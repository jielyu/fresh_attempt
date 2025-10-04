# encoding: utf-8

import example


def test_create_config():
    print(f"create_config: {example.create_config()}")


def test_print_json():
    config = {"a": 1, "b": "hello"}
    example.print_json(config)


def main():
    test_create_config()
    test_print_json()


if __name__ == "__main__":
    main()

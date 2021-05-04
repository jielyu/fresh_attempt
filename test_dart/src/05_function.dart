// 普通函数
int func1(int a) {
  print('func1');
  return 0;
}

// 不约束输出类型的函数
func2(int a) {
  print('func2');
  return 0;
}

// 不约束输入类型的函数
func3(a) {
  print('func3');
  return 0;
}

// 可选参数和带默认值的函数
int func4(int a, [int? b, int c = 4]) {
  print('func4, b=$b, c=$c');
  return 0;
}

// 键值对参数
int func5(int a, {int? d = 4, int e = 5}) {
  print('func5, b=$d, c=$e');
  return 0;
}

// 匿名函数
int func6() {
  var f = () {
    print('func6中的匿名函数');
  };
  f();
  return 0;
}

void main() {
  func1(10);
  func2(10);
  func3(10);
  func4(10, 2);
  func5(10, d: 2);
  func6();
}

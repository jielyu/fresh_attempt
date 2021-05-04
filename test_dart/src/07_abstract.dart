abstract class A {
  int id = 0;
  int func();
}

class B extends A {
  // 必须实现成员方法
  @override
  int func() {
    print('B实现A中的方法, id=${this.id}');
    return 0;
  }
}

class C implements A {
  // 必须覆盖所有成员，包括属性成员
  @override
  int id = 12;

  @override
  int func() {
    print('C实现A中的方法, id=${this.id}');
    return 0;
  }
}

void main(List<String> args) {
  //var a = A(); //编译错误，抽象类不允许实例化
  //
  var b = B();
  b.func(); // B实现A中的方法, id=0

  var c = C();
  c.func(); // C实现A中的方法, id=12
}

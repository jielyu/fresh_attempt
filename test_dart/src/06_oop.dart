class A {
  String _name = '';
  int _id = 0;

  // 一般构造函数
  A(this._name, this._id) {}
  // 命名构造函数
  A.name(this._name) {}
  A.id(this._id) {}

  // get, set
  get get_id {
    return this._id;
  }

  set set_id(int id) {
    this._id = id;
  }

  func() {
    print('A中的func, name=${this._name}, id=${this._id}');
  }
}

class B extends A {
  B(String name, int id) : super(name, id);

  @override
  func() {
    print('B中的func, name=${this._name}, id=${this._id}');
  }

  static int score = 99;

  static void f() {
    print('B中的静态方法, 静态成员score=${score}');
  }
}

void main() {
  // 封装
  var a = A('jack', 20);
  a.func();
  var a2 = A.id(20);
  a2.func();
  print(a2.get_id);
  a2.set_id = 10;
  print(a2.get_id);

  // 继承
  var b = B('hello', 5);
  b.func();

  // 多态
  A aa = new B('hello', 5);
  aa.func();

  // 静态方法和静态成员
  B.f();

  // 类型判断
  print(a is A); // true
  print(a is B); // false
  print(b is A); // true
  print(aa is A); // true
  print(aa is B); // true
}

T func<T>(T x) {
  return x;
}

class A<T> {
  T? x;

  A(this.x) {}

  func() {
    print('范型类A中的x=${this.x}');
  }
}

void main(List<String> args) {
  print(func<int>(10));

  var a = A(10);
  a.func();

  var aa = A("hello");
  aa.func();
}

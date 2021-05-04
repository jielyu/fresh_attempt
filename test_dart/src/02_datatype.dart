void main() {
  // 数值类型
  num a = 1;
  print(a is int);
  num b = 1.2;
  print(b is double);

  // 字符串
  var c = '你可以创建'
      '多行的字符串';
  String d = '指定具体类型';
  print('$c $d');

  // bool类型
  var e = false;
  var f = true;
  print('$e $f');

  // 数组
  var g = [1, 2, 3, 4];
  print('${g.length}, $g');

  // 集合
  var h = {'A', 'B', 'C', 'A'};
  print(h);

  // 词典
  var i = {'A': "Hello", 'B': 'World'};
  print(i);
  print(i.keys);
  print(i.values);
  print(i['A']);

  // 运算符
  var aa = 1 + 1;
  var bb = 2 * 3;
  var cc = 3 - 2;
  var dd = 6 / 3;
  var ee = 7 % 2;
  print('$aa $bb $cc $dd $ee');

  // 移位
  var ff = 2 << 1;
  var gg = 2 >> 1;
  print('$ff $gg');

  // 问号表达式
  var hh = 2 > 1 ? true : false;
  print('$hh');

  // 逻辑运算符
  var x = true && false;
  var y = true || false;
  var z = !true;
  print('$x $y $z');

  // 位运算符
  var xx = 6 & 1;
  var yy = 6 | 1;
  var zz = ~1;
  print('$xx $yy $zz');
}

void main() {
  // List
  var list = [1, 2, 3, 4, 5];
  list.insert(2, 5);
  print(list);
  var sum = 0;
  list.forEach((element) {
    sum += element;
  });
  print(sum);

  // set
  var s = new Set();
  s.add('A');
  s.add('B');
  s.add('A');
  print(s);
  s.forEach((element) {
    print(element);
  });

  // map
  var map = new Map();
  map['A'] = "hello";
  map['B'] = "world";
  print(map);
  map.forEach((key, value) {
    print('$key $value');
  });
}

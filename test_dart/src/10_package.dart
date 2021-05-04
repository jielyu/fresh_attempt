import "dart:math";
import "lib/mylib.dart";
import 'package:path/path.dart' as p;

void main(List<String> args) {
  print(min(1, 2));
  MyLib().func();
  print(p.join('home', 'test', 'document')); // home/test/document
}

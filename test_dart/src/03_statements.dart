void main() {
  // 分支语句
  if (true) {
    print('true branch');
  } else {
    print('false branch');
  }

  // switch语句
  var i = 1;
  switch (i) {
    case 0:
      print('case 0');
      break;
    case 1:
      print('case 1');
      break;
    default:
      print('default case');
  }

  // for循环语句
  int sum = 0;
  for (int i = 1; i <= 100; ++i) {
    sum += i;
  }
  print(sum);

  // while循环语句
  sum = 0;
  int j = 1;
  while (j <= 100) {
    sum += j;
    ++j;
  }
  print(sum);

  // do...while循环语句
  sum = 0;
  int k = 0;
  do {
    k++;
    sum += k;
  } while (k < 100);
  print(sum);

  // break和continue
  sum = 0;
  for (int i = 1; i < 10000; ++i) {
    if (50 == i) {
      continue;
    }
    if (i > 100) {
      break;
    }
    sum += i;
  }
  print(sum);

  // foreach
  sum = 0;
  var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  arr.forEach((i) {
    sum += i;
  });
  print(sum);
}

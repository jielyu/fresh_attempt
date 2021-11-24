import 'package:flutter/material.dart';
import 'src/home_page.dart';

class FreshmanSample extends StatelessWidget {
  const FreshmanSample({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "测试",
      routes: allRoutes,
      home: const HomePage(),
    );
  }
}

void main() {
  runApp(const FreshmanSample());
}

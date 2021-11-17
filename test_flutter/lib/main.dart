import 'package:flutter/material.dart';
import 'package:dotted_line/dotted_line.dart';
import 'src/test_sensor.dart';

// 定义合管理路由项目
class RouterItem {
  final String name;
  final String route;
  final WidgetBuilder builder;

  RouterItem({required this.name, required this.route, required this.builder});
}

// 定义路由导航
class RouteNavItem extends StatelessWidget {
  final RouterItem route;

  const RouteNavItem({required this.route, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(route.name),
      onTap: () {
        Navigator.pushNamed(context, route.route);
      },
    );
  }
}

// Widget相关的路由项目

// 传感器相关的路由项目
final sensorRoutes = [
  RouterItem(
      name: 'TestSensor',
      route: TestSensor.routeName,
      builder: (context) => const TestSensor()),
];
final sensorRouteMap =
    Map.fromEntries(sensorRoutes.map((e) => MapEntry(e.route, e.builder)));

// 所有路由设置
final allRoutes = <String, WidgetBuilder>{
  ...sensorRouteMap,
};

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("测试"),
      ),
      body: ListView(
        children: [
          ListTile(
              title: Text(
            "Widgets",
            style: Theme.of(context).textTheme.headline5,
            textAlign: TextAlign.center,
          )),
          const DottedLine(),
          ListTile(
              title: Text(
            "Sensors",
            style: Theme.of(context).textTheme.headline5,
            textAlign: TextAlign.center,
          )),
          ...sensorRoutes.map((e) => RouteNavItem(route: e)),
        ],
      ),
    );
  }
}

class FreshmanSample extends StatelessWidget {
  const FreshmanSample({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "功能测试",
      routes: allRoutes,
      home: const HomePage(),
    );
  }
}

void main() {
  runApp(const FreshmanSample());
}

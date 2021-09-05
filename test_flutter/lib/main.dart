import 'package:flutter/material.dart';

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

final sensorRoutes = [
  RouterItem(
      name: 'TestSensor',
      route: TestSensor.route_name,
      builder: (context) => const TestSensor()),
];

final sensorRouteMap =
    Map.fromEntries(sensorRoutes.map((e) => MapEntry(e.route, e.builder)));

final allRoutes = <String, WidgetBuilder>{
  ...sensorRouteMap,
};

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Sensor Samples1"),
      ),
      body: ListView(
        children: [
          ListTile(
              title: Text(
            "Sensors",
            style: Theme.of(context).textTheme.headline3,
          )),
          ...sensorRoutes.map((e) => RouteNavItem(route: e)),
        ],
      ),
    );
  }
}

class SensorSample extends StatelessWidget {
  const SensorSample({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Sensor Samples2",
      routes: allRoutes,
      home: const HomePage(),
    );
  }
}

void main() {
  runApp(const SensorSample());
}

import 'package:flutter/material.dart';
import 'package:dotted_line/dotted_line.dart';
import 'test_sensor.dart';
import 'test_widget.dart';

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
final widgetRoutes = [
  RouterItem(
      name: TextDemo.name,
      route: TextDemo.routeName,
      builder: (context) => const TextDemo()),
  RouterItem(
      name: ContainerDemo.name,
      route: ContainerDemo.routeName,
      builder: (context) => const ContainerDemo()),
  RouterItem(
      name: ColRowDemo.name,
      route: ColRowDemo.routeName,
      builder: (context) => const ColRowDemo()),
  RouterItem(
      name: ButtonDemo.name,
      route: ButtonDemo.routeName,
      builder: (context) => const ButtonDemo()),
  RouterItem(
      name: IconDemo.name,
      route: IconDemo.routeName,
      builder: (context) => const IconDemo()),
  RouterItem(
      name: ImageDemo.name,
      route: ImageDemo.routeName,
      builder: (context) => const ImageDemo()),
  RouterItem(
      name: AlignDemo.name,
      route: AlignDemo.routeName,
      builder: (context) => const AlignDemo()),
  RouterItem(
      name: AspectRatioDemo.name,
      route: AspectRatioDemo.routeName,
      builder: (context) => const AspectRatioDemo()),
  RouterItem(
      name: TransformDemo.name,
      route: TransformDemo.routeName,
      builder: (context) => const TransformDemo()),
  RouterItem(
      name: AutocompleteDemo.name,
      route: AutocompleteDemo.routeName,
      builder: (context) => const AutocompleteDemo()),
  RouterItem(
      name: FormDemo.name,
      route: FormDemo.routeName,
      builder: (context) => const FormDemo()),
  RouterItem(
      name: GridViewDemo.name,
      route: GridViewDemo.routeName,
      builder: (context) => const GridViewDemo()),
];
final widgetRouteMap =
    Map.fromEntries(widgetRoutes.map((e) => MapEntry(e.route, e.builder)));

// 传感器相关的路由项目
final sensorRoutes = [
  RouterItem(
      name: TestSensor.name,
      route: TestSensor.routeName,
      builder: (context) => const TestSensor()),
];
final sensorRouteMap =
    Map.fromEntries(sensorRoutes.map((e) => MapEntry(e.route, e.builder)));

// 所有路由设置
final allRoutes = <String, WidgetBuilder>{
  ...sensorRouteMap,
  ...widgetRouteMap,
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
            "Widgets示例",
            style: Theme.of(context).textTheme.headline5,
            textAlign: TextAlign.center,
          )),
          ...widgetRoutes.map((e) => RouteNavItem(route: e)),
          const DottedLine(),
          ListTile(
              title: Text(
            "传感器示例",
            style: Theme.of(context).textTheme.headline5,
            textAlign: TextAlign.center,
          )),
          ...sensorRoutes.map((e) => RouteNavItem(route: e)),
        ],
      ),
    );
  }
}

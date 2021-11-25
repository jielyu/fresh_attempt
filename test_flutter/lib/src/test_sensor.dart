import 'package:flutter/material.dart';

class TestSensor extends StatefulWidget {
  const TestSensor({Key? key}) : super(key: key);
  static const String name = 'Test Sensor';
  static const String routeName = '/sensors/test_sensor';

  @override
  TestSensorContainer createState() => TestSensorContainer();
}

class TestSensorContainer extends State<TestSensor> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Test Sensor"),
      ),
      body: const Text(
        "Hello Sensor",
        style: TextStyle(
          fontSize: 40,
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';

/// Text控件的Demo
class TextDemo extends StatelessWidget {
  static const String name = "Text Demo";
  static const String routeName = "/widget/text";

  const TextDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: const Text(
        "Text控件的例子",
        style: TextStyle(
          fontSize: 40,
          fontWeight: FontWeight.bold,
          color: Color.fromARGB(255, 255, 0, 255),
          backgroundColor: Color.fromARGB(255, 128, 128, 128),
        ),
      ),
    );
  }
}

/// Container控件的Demo
class ContainerDemo extends StatelessWidget {
  static const String name = "Container Demo";
  static const String routeName = "/widget/container";
  const ContainerDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text(name),
        ),
        body: Center(
          child: Container(
            color: const Color.fromARGB(255, 128, 128, 128),
            child: const Text('container会充满父窗口'),
            alignment: Alignment.center,
          ),
        ));
  }
}

/// Column和Row布局控件的Demo
class ColRowDemo extends StatelessWidget {
  static const String name = "ColRow Demo";
  static const String routeName = "/widget/colrow";
  const ColRowDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text(name),
        ),
        body: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: <Widget>[
            Row(
              //crossAxisAlignment: CrossAxisAlignment.stretch,
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: <Widget>[
                Container(
                  color: Colors.blue,
                  child: const Center(
                    child: Text(
                      '1',
                      textAlign: TextAlign.center,
                    ),
                  ),
                  height: 50,
                  width: 50,
                ),
                Container(
                  color: Colors.blue,
                  child: const Text(
                    '2',
                    textAlign: TextAlign.center,
                  ),
                  height: 50,
                  width: 50,
                ),
                Container(
                  color: Colors.blue,
                  child: const Text(
                    '3',
                    textAlign: TextAlign.center,
                  ),
                  height: 50,
                  width: 50,
                )
              ],
            ),
            Row(
              //crossAxisAlignment: CrossAxisAlignment.stretch,
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: <Widget>[
                Container(
                  color: Colors.green,
                  child: const Text(
                    '4',
                    textAlign: TextAlign.center,
                  ),
                  height: 50,
                  width: 50,
                ),
                Container(
                  color: Colors.pink,
                  child: const Text(
                    '5',
                    textAlign: TextAlign.center,
                  ),
                  height: 50,
                  width: 50,
                ),
                Container(
                  color: Colors.blueGrey,
                  child: const Text(
                    '6',
                    textAlign: TextAlign.center,
                  ),
                  height: 50,
                  width: 50,
                )
              ],
            ),
          ],
        ));
  }
}

/// Button类型空间的Demo
class ButtonDemo extends StatefulWidget {
  static const String name = "Button Demo";
  static const String routeName = "/widget/button";
  const ButtonDemo({Key? key}) : super(key: key);

  @override
  _ButtonDemoState createState() => _ButtonDemoState();
}

class _ButtonDemoState extends State<ButtonDemo> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Button Demo"),
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            const ElevatedButton(
                onPressed: null,
                child: Text(
                  'Disable',
                  style: TextStyle(color: Colors.yellow),
                )),
            const SizedBox(height: 30),
            ElevatedButton(
                onPressed: () {
                  // ignore: avoid_print
                  print('click enable');
                },
                child: const Text('Enable'))
          ],
        ),
      ),
    );
  }
}

/// Icon控件的Demo
class IconDemo extends StatelessWidget {
  static const String name = "Icon Demo";
  static const String routeName = "/widget/icon";
  const IconDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: const <Widget>[
          Icon(
            Icons.favorite,
            color: Colors.pink,
            size: 24.0,
            semanticLabel: 'Text to announce in accessibility modes',
          ),
          Icon(
            Icons.audiotrack,
            color: Colors.green,
            size: 30.0,
          ),
          Icon(
            Icons.beach_access,
            color: Colors.blue,
            size: 36.0,
          ),
        ],
      ),
    );
  }
}

/// Image控件的Demo
class ImageDemo extends StatelessWidget {
  static const String name = "Image Demo";
  static const String routeName = "/widget/image";
  const ImageDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: const Image(
        /// 需要在文件 macos/Runner/DebugProfile.entitlements 中添加
        /// <key>com.apple.security.network.client</key>
        /// <true/>
        image: NetworkImage('https://blog.bluegeek.me/img/portrait.png'),
      ),
    );
  }
}

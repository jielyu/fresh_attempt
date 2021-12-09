import 'package:flutter/material.dart';
import 'dart:math' as math;

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

class AlignDemo extends StatelessWidget {
  static const String name = "Align Demo";
  static const String routeName = "/widget/align";
  const AlignDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: Column(
        children: [
          Center(
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 20.0),
              height: 120.0,
              width: 120.0,
              color: Colors.blue[50],
              child: const Align(
                alignment: Alignment.topRight,
                child: FlutterLogo(
                  size: 60,
                ),
              ),
            ),
          ),
          Center(
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 20.0),
              height: 120.0,
              width: 120.0,
              color: Colors.blue[50],
              child: const Align(
                alignment: Alignment(0.2, 0.6),
                child: FlutterLogo(
                  size: 60,
                ),
              ),
            ),
          ),
          Center(
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 20.0),
              height: 120.0,
              width: 120.0,
              color: Colors.blue[50],
              child: const Align(
                alignment: FractionalOffset(0.2, 0.6),
                child: FlutterLogo(
                  size: 60,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class AspectRatioDemo extends StatelessWidget {
  static const String name = "Aspect Ratio Demo";
  static const String routeName = "/widget/aspectratio";
  const AspectRatioDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: Column(
        children: [
          Container(
            margin: const EdgeInsets.symmetric(vertical: 20),
            color: Colors.blue,
            alignment: Alignment.center,
            width: double.infinity,
            height: 300.0,
            child: AspectRatio(
              aspectRatio: 16 / 9,
              child: Container(
                color: Colors.green,
              ),
            ),
          ),
          Container(
            margin: const EdgeInsets.symmetric(vertical: 20),
            color: Colors.blue,
            alignment: Alignment.center,
            width: 100.0,
            height: 100.0,
            child: AspectRatio(
              aspectRatio: 2.0,
              child: Container(
                width: 100.0,
                height: 50.0,
                color: Colors.green,
              ),
            ),
          ),
          Container(
            margin: const EdgeInsets.symmetric(vertical: 20),
            color: Colors.blue,
            alignment: Alignment.center,
            width: 100.0,
            height: 100.0,
            child: AspectRatio(
              aspectRatio: 0.5,
              child: Container(
                width: 100.0,
                height: 50.0,
                color: Colors.green,
              ),
            ),
          )
        ],
      ),
    );
  }
}

class TransformDemo extends StatelessWidget {
  static const String name = "Transform Demo";
  static const String routeName = "/widget/transform";
  const TransformDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: Column(
        children: [
          Transform(
            alignment: Alignment.bottomCenter,
            transform: Matrix4.skewY(0.3)..rotateZ(-math.pi / 6.0),
            child: Container(
              margin:
                  const EdgeInsets.symmetric(vertical: 100, horizontal: 100),
              padding: const EdgeInsets.all(8.0),
              color: Colors.blue,
              child: const Text('Apartment for rent!'),
            ),
          ),
        ],
      ),
    );
  }
}

class AutocompleteDemo extends StatelessWidget {
  static const String name = "Autocomplete Demo";
  static const String routeName = "/widget/autocompleteDemom";
  const AutocompleteDemo({Key? key}) : super(key: key);

  static const List<String> _kOptions = <String>[
    'aardvark',
    'bobcat',
    'chameleon',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text(name)),
        body: Container(
          margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 100),
          child: Autocomplete<String>(
            optionsBuilder: (TextEditingValue textEditingValue) {
              if (textEditingValue.text == '') {
                return const Iterable<String>.empty();
              }
              return _kOptions.where((String option) {
                return option.contains(textEditingValue.text.toLowerCase());
              });
            },
            onSelected: (String selection) {
              debugPrint('You just selected $selection');
            },
          ),
        ));
  }
}

class MyStatefulWidget extends StatefulWidget {
  const MyStatefulWidget({Key? key}) : super(key: key);

  @override
  State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          TextFormField(
            decoration: const InputDecoration(
              hintText: 'Enter your email',
            ),
            validator: (String? value) {
              if (value == null || value.isEmpty) {
                return 'Please enter some text';
              }
              return null;
            },
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: ElevatedButton(
              onPressed: () {
                // Validate will return true if the form is valid, or false if
                // the form is invalid.
                if (_formKey.currentState!.validate()) {
                  // ignore: avoid_print
                  print("clicked");
                }
              },
              child: const Center(
                child: Text('Submit'),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class FormDemo extends StatelessWidget {
  static const String name = "Form Demo";
  static const String routeName = "/widget/form";
  const FormDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: Container(
        margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
        child: const MyStatefulWidget(),
      ),
    );
  }
}

class GridViewDemo extends StatelessWidget {
  static const String name = "GridView Demo";
  static const String routeName = "/widget/gridgiew";
  const GridViewDemo({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(name),
      ),
      body: GridView.count(
        primary: false,
        padding: const EdgeInsets.all(20),
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        crossAxisCount: 3,
        children: <Widget>[
          Container(
            padding: const EdgeInsets.all(8),
            child: const Text("He'd have you all unravel at the"),
            color: Colors.teal[100],
          ),
          Container(
            padding: const EdgeInsets.all(8),
            child: const Text('Heed not the rabble'),
            color: Colors.teal[200],
          ),
          Container(
            padding: const EdgeInsets.all(8),
            child: const Text('Sound of screams but the'),
            color: Colors.teal[300],
          ),
          Container(
            padding: const EdgeInsets.all(8),
            child: const Text('Who scream'),
            color: Colors.teal[400],
          ),
          Container(
            padding: const EdgeInsets.all(8),
            child: const Text('Revolution is coming...'),
            color: Colors.teal[500],
          ),
          Container(
            padding: const EdgeInsets.all(8),
            child: const Text('Revolution, they...'),
            color: Colors.teal[600],
          ),
        ],
      ),
    );
  }
}

import 'package:desktop_window/desktop_window.dart';
import 'package:flutter/material.dart';
import 'formatting.dart';
import 'simulation.dart';
import 'graph.dart';


void main() {
  runApp(MyApp());
  testWindowFunctions();
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Meins',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        brightness: Brightness.dark,
        accentColor: Colors.orange[900],
        toggleableActiveColor:Colors.orange[900],
        elevatedButtonTheme: ElevatedButtonThemeData(style: ButtonStyle(backgroundColor: MaterialStateProperty.all(Colors.orange[900])))
      ),
      home: MyHomePage(title: 'Datenanalysetool v1.0.0'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: Text(widget.title),
          bottom: TabBar(
            tabs: [
              Tab(text: "Fromatieren"),
              Tab(text: "Aufstieg simulieren"),
              Tab(text: "Visuell darstellen"),
            ],
          ),
        ),
        body: TabBarView(children: [
          Formatting(),
          Simulations(),
          Plotting(),
        ]),
      ),
    );
  }
}

Future testWindowFunctions() async {
    await DesktopWindow.setFullScreen(true);
}
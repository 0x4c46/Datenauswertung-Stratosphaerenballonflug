import 'dart:convert';
import "package:flutter/material.dart";
import 'package:flutter/services.dart';
import 'package:file_selector_platform_interface/file_selector_platform_interface.dart';
import 'dart:io';

class Simulations extends StatefulWidget {
  @override
  _SimulationsState createState() => _SimulationsState();
}

class _SimulationsState extends State<Simulations> {
  bool isExperience = false;
  TextEditingController heController = TextEditingController();
  TextEditingController massController = TextEditingController();
  TextEditingController stopController = TextEditingController();
  TextEditingController filenameController = TextEditingController();
  String stopUnit = "Radius";
  String directory = "";
  String stdout = "a";
  String stderr = "";

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        RadioListTile(
          title: Text("Rein physikalische Berechnung"),
          value: false,
          groupValue: isExperience,
          onChanged: (bool value) {
            setState(() {
              isExperience = value;
            });
          },
        ),
        RadioListTile(
          title: Text("+ Erfahrungswerte vorheriger Flüge"),
          value: true,
          groupValue: isExperience,
          onChanged: (bool value) {
            setState(() {
              isExperience = value;
            });
          },
        ),
        ListTile(
          leading: Text("Speicherort:"),
          title: Row(
            children: [
              ElevatedButton(
                child: Text("Ordner auswählen"),
                onPressed: () async {
                  directory =
                      await FileSelectorPlatform.instance?.getDirectoryPath() ??
                          "";
                  setState(() {});
                },
              ),
              SizedBox(width: 10),
              if (directory != "")
                Icon(
                  Icons.check,
                  color: Colors.green,
                ),
              SizedBox(
                width: 20,
              ),
              SizedBox(
                width: 150,
                child: TextField(
                  onChanged: (_) => setState(() {}),
                  controller: filenameController,
                  decoration: InputDecoration(hintText: 'Dateiname'),
                ),
              ),
              Text(".csv"),
              SizedBox(
                width: 20,
              ),
              Text(directory)
            ],
          ),
        ),
        ListTile(
          leading: Text("Volumen Helium [m³]:"),
          title: Row(
            children: [
              SizedBox(
                width: 188,
                child: TextField(
                  onChanged: (_) => setState(() {}),
                  controller: heController,
                  inputFormatters: [
                    FilteringTextInputFormatter.allow(
                        RegExp("[0-9]+[.]?[0-9]*"))
                  ],
                  decoration: InputDecoration(hintText: "z.B. 2.345"),
                ),
              ),
            ],
          ),
        ),
        ListTile(
          leading: Text("Masse Nutzlast [kg]:"),
          title: Row(
            children: [
              SizedBox(
                width: 200,
                child: TextField(
                  onChanged: (_) => setState(() {}),
                  controller: massController,
                  inputFormatters: [
                    FilteringTextInputFormatter.allow(
                        RegExp("[0-9]+[.]?[0-9]*"))
                  ],
                  decoration: InputDecoration(hintText: "z.B. 2.345"),
                ),
              ),
            ],
          ),
        ),
        ListTile(
          leading: Text("Ende:"),
          title: Row(
            children: [
              DropdownButton<String>(
                value: stopUnit,
                isDense: true,
                onChanged: (String value) {
                  setState(() => stopUnit = value);
                },
                items: ["Radius", "Höhe"]
                    .map(
                      (e) => DropdownMenuItem(
                        child: Text(e),
                        value: e,
                      ),
                    )
                    .toList(),
              ),
              SizedBox(
                width: 100,
                child: TextField(
                  onChanged: (_) => setState(() {}),
                  controller: stopController,
                  inputFormatters: [
                    FilteringTextInputFormatter.allow(
                        RegExp("[0-9]+[.]?[0-9]*")),
                  ],
                ),
              ),
              Text("Meter"),
              SizedBox(
                width: 20,
              ),
              Tooltip(
                message:
                    "Platzradius:\n Wetterballon 200: 1.5m \n Wetterballon 800: 3.40m \n Wetterballon 1600: 5.25m \n Wetterballon 2000: 5.5m \n Wetterballon 3000: 6.25m",
                child: Icon(
                  Icons.help_outline,
                  color: Colors.black54,
                ),
              ),
            ],
          ),
        ),
        ListTile(
          title: ElevatedButton(
            child: allSet()
                ? Text("Run")
                : Text(
                    "Bitte zuerst alle Felder ausfüllen!",
                    style: TextStyle(color: Colors.black87),
                  ),
            onPressed: allSet() ? run : null,
          ),
        ),
        if (stdout == "" && stderr == "") ...[
          ListTile(
            leading: Text("Loading..."),
            title: LinearProgressIndicator(),
          ),
          ListTile(
            title: Text("Dieser Vorgang kann einige Sekunden dauern."),
          ),
        ],
        if (stdout.contains("overflow error")) ...[
          ListTile(
              leading: Text(
                "ERROR:",
                style: TextStyle(color: Colors.red),
              ),
              title: Text(stdout.replaceAll("\n", ""))),
          ListTile(leading: Text("Bitte überprüfe deine Eingabe!"))
        ] else if (stdout.contains("Done"))
          ListTile(
            leading: Text(
                "Die Simulation ist ferig. Du findest sie hier: ${directory.replaceAll("\\", "/") + '/' + filenameController.text + ".csv"}"),
          )
        else if (stderr != "")
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Text("Bitte überprüfe Deine Eingabe!\n\n" + stderr),
          )
        else
          ListTile(
            leading: Text(""),
          )
      ],
    );
  }

  bool allSet() {
    return heController.text != "" &&
        massController.text != "" &&
        stopController.text != "" &&
        filenameController.text != "" &&
        directory != "";
  }

  void run() async {
    String command =
        "simulate!!${directory.replaceAll("\\", "/") + '/' + filenameController.text + ".csv"}!!${heController.text}!!${massController.text}!!$stopUnit!!${stopController.text}!!$isExperience";
    var res = await Process.start("data/flutter_assets/assets/main.exe", []);
    res.stdin.writeln(command);
    setState(() {
      stdout = "";
      stderr = "";
    });
    res.stdout.transform(utf8.decoder).forEach((a) => setState(() {
          stdout = a;
        }));
    res.stderr.transform(utf8.decoder).forEach((b) => setState(() {
          stderr = b;
        }));
  }
}

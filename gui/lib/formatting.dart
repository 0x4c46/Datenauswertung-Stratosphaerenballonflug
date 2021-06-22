import "package:flutter/material.dart";
import 'package:flutter_datetime_picker/flutter_datetime_picker.dart';
import 'package:file_selector_platform_interface/file_selector_platform_interface.dart';
import 'dart:convert';
import 'dart:io';

class Formatting extends StatefulWidget {
  @override
  _FormattingState createState() => _FormattingState();
}

class _FormattingState extends State<Formatting> {
  bool isStrato = true;
  DateTime startDate = DateTime.now();
  DateTime landDate = DateTime.now();
  TextEditingController delimiterController = TextEditingController()
    ..text = ",";
  TextEditingController filenameController = TextEditingController();
  String directory = "";
  String file = "";
  bool tickedStarted = false;
  bool tickedLanded = false;
  String stderr = "";
  String stdout = "a";

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        RadioListTile(
          title: Text("Strato 3"),
          value: true,
          groupValue: isStrato,
          onChanged: (bool value) {
            setState(() {
              isStrato = value;
            });
          },
        ),
        RadioListTile(
          title: Text("Arduino"),
          value: false,
          groupValue: isStrato,
          onChanged: (bool value) {
            setState(() {
              isStrato = value;
              tickedStarted = true;
              tickedLanded = true;
            });
          },
        ),
        ListTile(
          leading: Text("Rohdatei:"),
          title: Row(
            children: [
              ElevatedButton(
                child: Text("Datei auswählen"),
                onPressed: () async {
                  XFile xFile = await FileSelectorPlatform.instance?.openFile();
                  setState(() => file = xFile.path);
                },
              ),
              SizedBox(
                width: 20,
              ),
              Text(file),
            ],
          ),
        ),
        ListTile(
          leading: Text("Formatierte Datei:"),
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
                  controller: filenameController,
                  onChanged: (_) => setState(() {}),
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
        CheckboxListTile(
          value: tickedStarted,
          controlAffinity: ListTileControlAffinity.leading,
          title: Row(
            children: [
              Text("Startzeit (UTC): "),
              SizedBox(
                width: 20,
              ),
              ElevatedButton(
                child: Text("Zeit auswählen"),
                onPressed: () {
                  DatePicker.showTimePicker(
                    context,
                    currentTime: startDate,
                    onChanged: (DateTime date) {
                      setState(() => this.startDate = date);
                    },
                  );
                },
              ),
              SizedBox(
                width: 20,
              ),
              Text("${startDate.hour}:${startDate.minute}:${startDate.second}"),
            ],
          ),
          onChanged: (bool newvalue) {
            if (isStrato) {
              setState(() {
                tickedStarted = newvalue;
              });
            }
          },
        ),
        CheckboxListTile(
          value: tickedLanded,
          controlAffinity: ListTileControlAffinity.leading,
          title: Row(
            children: [
              Text("Landezeit (UTC): "),
              SizedBox(
                width: 20,
              ),
              ElevatedButton(
                child: Text("Zeit auswählen"),
                onPressed: () {
                  DatePicker.showTimePicker(
                    context,
                    currentTime: landDate,
                    onChanged: (DateTime date) {
                      setState(() => this.landDate = date);
                    },
                  );
                },
              ),
              SizedBox(
                width: 20,
              ),
              Text("${landDate.hour}:${landDate.minute}:${landDate.second}"),
            ],
          ),
          onChanged: (bool newvalue) {
            if (isStrato) {
              setState(() {
                tickedLanded = newvalue;
              });
            }
          },
        ),
        ListTile(
          leading: Text("Trennzeichen:"),
          title: Row(
            children: [
              SizedBox(
                width: 200,
                child: TextField(
                  maxLength: 1,
                  onChanged: (_) => setState(() {}),
                  controller: delimiterController,
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
        if (stderr != "")
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Text(
                "Bitte überprüfe Deine Eingabe! Die Rohdatei darf nicht verändert worden sein!\n\n" +
                    stderr),
          ),
        if (stdout.contains("Done"))
          ListTile(
            leading: Text(
                "Die Formatierung ist ferig. Du findest die Datei hier: ${directory.replaceAll("\\", "/") + '/' + filenameController.text + ".csv"}"),
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
      ],
    );
  }

  bool allSet() {
    return delimiterController.text != "" &&
        filenameController.text != "" &&
        file != "" &&
        directory != "";
  }

  void run() async {
    String command =
        "format!!$isStrato!!${file.replaceAll("\\", "/")}!!${directory.replaceAll("\\", "/") + '/' + filenameController.text + ".csv"}!!${tickedStarted ? startDate.hour + startDate.minute / 60 + startDate.second / 3600 : 25}!!${tickedLanded ? landDate.hour + landDate.minute / 60 + landDate.second / 3600 : 25}!!${delimiterController.text}";
    var res = await Process.start("data/flutter_assets/assets/main.exe", []);
    res.stdin.writeln(command);
    setState(() {
      stderr = "";
      stdout = "";
    });
    res.stderr.transform(utf8.decoder).forEach((b) => setState(() {
          stderr = b;
        }));
    res.stdout.transform(utf8.decoder).forEach((c) => setState(() {
          stdout = c;
        }));
  }
}

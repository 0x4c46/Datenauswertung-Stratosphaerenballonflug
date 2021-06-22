import 'dart:convert';
import "package:flutter/material.dart";
import 'package:gui/datarow.dart';
import 'dart:io';

enum ValType { stratVal, preVal, ardVal }

class Plotting extends StatefulWidget {
  @override
  _PlottingState createState() => _PlottingState();
}

class _PlottingState extends State<Plotting> {
  TextEditingController titleController = TextEditingController();
  bool is3D = false;
  bool onlyUp = false;
  bool autosizedAxis = true;
  String stderr = "";
  DataRow dataRow1 = DataRow();
  DataRow dataRow2 = DataRow();
  DataRow dataRow3 = DataRow();

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        ListTile(
          leading: Text("Titel des Graphen:"),
          title: Row(
            children: [
              SizedBox(
                width: 400,
                child: TextField(
                  onChanged: (_) => setState(() {}),
                  controller: titleController,
                ),
              ),
            ],
          ),
        ),
        RadioListTile(
          title: Text("2D"),
          value: false,
          groupValue: is3D,
          onChanged: (bool value) {
            setState(
              () {
                is3D = value;
              },
            );
          },
        ),
        RadioListTile(
          title: Text("3D"),
          value: true,
          groupValue: is3D,
          onChanged: (bool value) {
            setState(
              () {
                is3D = value;
              },
            );
          },
        ),
        CheckboxListTile(
          value: onlyUp,
          controlAffinity: ListTileControlAffinity.leading,
          title: Row(
            children: [
              Text("Nur Aufstieg plotten"),
              SizedBox(
                width: 10,
              ),
              Tooltip(
                message: "Nur Strato",
                child: Icon(
                  Icons.help_outline,
                  color: Colors.black54,
                ),
              ),
            ],
          ),
          onChanged: (bool value) {
            setState(
              () {
                onlyUp = value;
              },
            );
          },
        ),
        // CheckboxListTile(
        //   value: autosizedAxis,
        //   controlAffinity: ListTileControlAffinity.leading,
        //   title: Text("Achsen automatisch skallieren"),
        //   onChanged: (bool value) {
        //     setState(
        //       () {
        //         autosizedAxis = value;
        //       },
        //     );
        //   },
        // ),// not working well, xlim and ylim necessary
        SizedBox(
          height: 20,
        ),
        DataRowWidget(dataRow1, dataRow2, dataRow3, is3D, setState),
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
                "Bitte überprüfe Deine Eingabe!\n\n" +
                    stderr),
          )
      ],
    );
  }

  bool allSet() {
    bool row1 = dataRow1.file != "" &&
        dataRow1.xValue != null &&
        dataRow1.yValue != null &&
        dataRow1.filterController.text != "" &&
        dataRow1.sizeController.text != "" &&
        (is3D ? dataRow1.zValue != null : true);
    bool row2 = dataRow2.activated
        ? (dataRow2.file != "" &&
            dataRow2.xValue != null &&
            dataRow2.yValue != null &&
            dataRow2.filterController.text != "" &&
            dataRow2.sizeController.text != "" &&
            (is3D ? dataRow2.zValue != null : true))
        : true;
    bool row3 = dataRow3.activated
        ? (dataRow3.file != "" &&
            dataRow3.xValue != null &&
            dataRow3.yValue != null &&
            dataRow3.filterController.text != "" &&
            dataRow3.sizeController.text != "" &&
            (is3D ? dataRow3.zValue != null : true))
        : true;
    return row1 && row2 && row3;
  }

  void run() async {
    String graphOptions =
        "${titleController.text}!!$is3D!!$onlyUp!!$autosizedAxis!!";
    String datastream1 =
        "${dataRow1.activated}!!${dataRow1.valType.toString().split(".").last}!!${dataRow1.xValue}!!${dataRow1.yValue}!!${dataRow1.labelController.text}!!${dataRow1.file?.replaceAll("\\", "/")}!!${dataRow1.color}!!${dataRow1.sizeController.text}!!${dataRow1.isScatter}!!${dataRow1.zValue}!!${dataRow1.filterController.text}!!";
    String datastream2 =
        "${dataRow2.activated}!!${dataRow2.valType.toString().split(".").last}!!${dataRow2.xValue}!!${dataRow2.yValue}!!${dataRow2.labelController.text}!!${dataRow2.file?.replaceAll("\\", "/")}!!${dataRow2.color}!!${dataRow2.sizeController.text}!!${dataRow2.isScatter}!!${dataRow2.zValue}!!${dataRow2.filterController.text}!!";
    String datastream3 =
        "${dataRow3.activated}!!${dataRow3.valType.toString().split(".").last}!!${dataRow3.xValue}!!${dataRow3.yValue}!!${dataRow3.labelController.text}!!${dataRow3.file?.replaceAll("\\", "/")}!!${dataRow3.color}!!${dataRow3.sizeController.text}!!${dataRow3.isScatter}!!${dataRow3.zValue}!!${dataRow3.filterController.text}";
    String command =
        "plot!!" + graphOptions + datastream1 + datastream2 + datastream3;
    print(command);
    var res = await Process.start("data/flutter_assets/assets/main.exe", []);
    res.stdin.writeln(command);
    res.stdout.transform(utf8.decoder).forEach(print);
    setState(() {
      stderr = "";
    });
    res.stderr.transform(utf8.decoder).forEach((b) => setState(() {
          stderr = b;
        }));
  }
}

class DataRow {
  bool activated = false;
  ValType valType = ValType.stratVal;
  String xValue;
  String yValue;
  TextEditingController labelController = TextEditingController();
  String file;
  String color = "r";
  TextEditingController sizeController = TextEditingController();
  bool isScatter = true;
  String zValue;
  TextEditingController filterController = TextEditingController() ..text = "1";
}

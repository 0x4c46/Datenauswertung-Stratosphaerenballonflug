import 'package:flutter/material.dart';
import 'graph.dart' as graph;
import 'package:flutter/services.dart';
import 'package:file_selector_platform_interface/file_selector_platform_interface.dart';
import 'lists.dart';

class DataRowWidget extends StatelessWidget {
  graph.DataRow dataRow1;
  graph.DataRow dataRow2;
  graph.DataRow dataRow3;
  bool is3D;
  dynamic setState;
  DataRowWidget(
      this.dataRow1, this.dataRow2, this.dataRow3, this.is3D, this.setState);
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        dataRow1,
        dataRow2,
        dataRow3,
      ]
          .map(
            (dataRow) => Expanded(
              child: Column(
                children: [
                  Text(
                    "Datenreihe",
                    textScaleFactor: 1.8,
                  ),
                  Switch(
                    value: dataRow.activated,
                    onChanged: (bool value) {
                      setState(
                        () {
                          dataRow.activated = value;
                        },
                      );
                    },
                  ),
                  AnimatedOpacity(
                    opacity: dataRow.activated ? 1 : 0.2,
                    duration: Duration(milliseconds: 200),
                    child: Column(
                      children: [
                        RadioListTile(
                          title: Text("Simulation"),
                          value: graph.ValType.preVal,
                          groupValue: dataRow.valType,
                          onChanged: (graph.ValType value) {
                            setState(() {
                              dataRow.valType = value;
                              dataRow.xValue = null;
                              dataRow.yValue = null;
                              dataRow.zValue = null;
                            });
                          },
                        ),
                        RadioListTile(
                          title: Text("Strato"),
                          value: graph.ValType.stratVal,
                          groupValue: dataRow.valType,
                          onChanged: (graph.ValType value) {
                            setState(() {
                              dataRow.valType = value;
                              dataRow.xValue = null;
                              dataRow.yValue = null;
                              dataRow.zValue = null;
                            });
                          },
                        ),
                        RadioListTile(
                          title: Text("Arduino"),
                          value: graph.ValType.ardVal,
                          groupValue: dataRow.valType,
                          onChanged: (graph.ValType value) {
                            setState(() {
                              dataRow.valType = value;
                              dataRow.xValue = null;
                              dataRow.yValue = null;
                              dataRow.zValue = null;
                            });
                          },
                        ),
                        ListTile(
                          leading: Text("Datei:"),
                          title: Row(
                            children: [
                              ElevatedButton(
                                child: Text(dataRow.file == null
                                    ? "Datei auswählen"
                                    : dataRow.file.split("\\").last),
                                onPressed: () async {
                                  XFile xFile = await FileSelectorPlatform
                                      .instance
                                      .openFile();
                                  setState(() => dataRow.file = xFile?.path);
                                },
                              ),
                              SizedBox(width: 10),
                              if (dataRow.file != null)
                                Icon(
                                  Icons.check,
                                  color: Colors.green,
                                )
                              else
                                Icon(
                                  Icons.warning_amber_rounded,
                                  color: Colors.red,
                                )
                            ],
                          ),
                        ),
                        ListTile(
                          leading: Text("Beschriftung:"),
                          title: Row(
                            children: [
                              SizedBox(
                                width: 150,
                                child: TextField(
                                    onChanged: (_) => setState(() {}),
                                    controller: dataRow.labelController),
                              ),
                            ],
                          ),
                        ),
                        buildUnitSelection(
                            dataRow, "x-Achse", dataRow.xValue, "x"),
                        buildUnitSelection(
                            dataRow, "y-Achse", dataRow.yValue, "y"),
                        if (is3D)
                          buildUnitSelection(
                              dataRow, "z-Achse", dataRow.zValue, "z"),
                        ListTile(
                          leading: Text("Farbe:"),
                          title: Row(
                            children: [
                              DropdownButton<String>(
                                value: dataRow.color,
                                isDense: true,
                                onChanged: (String value) {
                                  setState(() => dataRow.color = value);
                                },
                                items: [...colors]
                                    .map(
                                      (e) => DropdownMenuItem(
                                        child: Text(e.display),
                                        value: e.key,
                                      ),
                                    )
                                    .toList(),
                              ),
                            ],
                          ),
                        ),
                        ListTile(
                          leading: Text("Größe:"),
                          title: Row(
                            children: [
                              SizedBox(
                                width: 100,
                                child: TextField(
                                  onChanged: (_) => setState(() {}),
                                  controller: dataRow.sizeController,
                                  inputFormatters: [
                                    FilteringTextInputFormatter.allow(
                                        RegExp("[0-9]+[.]?[0-9]*"))
                                  ],
                                ),
                              ),
                              SizedBox(
                                width: 10,
                              ),
                              Tooltip(
                                message:
                                    "Übliche Werte liegen zwischen 1 und 10",
                                child: Icon(
                                  Icons.help_outline,
                                  color: Colors.black54,
                                ),
                              ),
                            ],
                          ),
                        ),
                        ListTile(
                          leading: Text("Filter:"),
                          title: Row(
                            children: [
                              Text("jeden "),
                              SizedBox(
                                width: 10,
                              ),
                              SizedBox(
                                width: 50,
                                child: TextField(
                                  onChanged: (_) => setState(() {}),
                                  controller: dataRow.filterController,
                                  inputFormatters: [
                                    FilteringTextInputFormatter.allow(
                                        RegExp("[0-9]*")),
                                  ],
                                ),
                              ),
                              Text(". Wert anzeigen"),
                              SizedBox(
                                width: 10,
                              ),
                              Tooltip(
                                message:
                                    "Es empfielt sich, maximal 100.000 Werte pro Datenreihe zu verwenden. \nKeinen Wert herausfiltern: 1",
                                child: Icon(
                                  Icons.help_outline,
                                  color: Colors.black54,
                                ),
                              ),
                            ],
                          ),
                        ),
                        RadioListTile(
                          title: Text("Linie"),
                          value: false,
                          groupValue: dataRow.isScatter,
                          onChanged: (bool value) {
                            setState(
                              () {
                                dataRow.isScatter = value;
                              },
                            );
                          },
                        ),
                        RadioListTile(
                          title: Text("gepunktet"),
                          value: true,
                          groupValue: dataRow.isScatter,
                          onChanged: (bool value) {
                            setState(
                              () {
                                dataRow.isScatter = value;
                              },
                            );
                          },
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          )
          .toList(),
    );
  }

  ListTile buildUnitSelection(
      graph.DataRow dataRow, String leading, String value, String unit) {
    return ListTile(
      leading: Text(leading),
      title: Row(
        children: [
          DropdownButton<String>(
            value: value,
            isDense: true,
            onChanged: (String value) {
              if (unit == "x")
                setState(() => dataRow.xValue = value);
              else if (unit == "y")
                setState(() => dataRow.yValue = value);
              else if (unit == "z") setState(() => dataRow.zValue = value);
            },
            items: [
              if (dataRow.valType == graph.ValType.preVal) ...preVal,
              if (dataRow.valType == graph.ValType.stratVal) ...stratVal,
              if (dataRow.valType == graph.ValType.ardVal) ...ardVal
            ]
                .map(
                  (e) => DropdownMenuItem(
                    child: Text(e.display),
                    value: e.key,
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }
}

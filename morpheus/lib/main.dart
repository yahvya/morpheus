import 'package:flutter/material.dart';
import 'package:morpheus/pages/Home.dart';

void main() {
  runApp(MaterialApp(
    title: "Morpheus",
    home: Home(),
    theme: ThemeData(
      // theme de l'application
      brightness: Brightness.dark
    ),
  ));
}

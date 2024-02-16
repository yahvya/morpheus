import 'package:flutter/material.dart';
import 'package:morpheus/pages/Home.dart';

void main() {
  runApp(MaterialApp(
    title: "Morpheus",
    home: Home(),
    theme: ThemeData(
      // theme de l'application
      //brightness: Brightness.dark,
      colorScheme: const ColorScheme(
        primary: Color(0xFF131313), // Le noir pour le fond
        secondary: Color(0xFF579647), // Le vert pour la mise en évidence d’éléments
        surface: Color(0xFFD0D2CF), // Le gris light pour les couleurs simples
        background: Color(0xFF1B1B1B), // Le noir light comme couleur pouvant aller au dessus du fond
        error: Colors.red, // Couleur d'erreur
        onPrimary: Color(0xFFFDFDFD), // Le blanc gris pour le texte
        onSecondary: Color(0xFFFDFDFD), // Le blanc gris pour le texte
        onSurface: Color(0xFFD0D2CF), // Le noir pour le fond
        onBackground: Color(0x001B1B1B), // Le blanc gris pour le texte
        onError: Color(0xFFFDFDFD), // Le blanc gris pour le texte
        brightness: Brightness.dark, // Luminosité de la palette de couleurs
      ),
    ),
  ));
}

import 'dart:ui';

import 'package:flutter/material.dart';

/// @brief Thème couleur de l'application
enum AppTheme{
  /// @brief Couleur de fond de l'application
  backgroundColor(color: Color.fromRGBO(26, 26, 33, 1.0)),

  /// @brief Couleur du texte sur "backgroundColor"
  textColor(color: Color.fromRGBO(255, 255, 255, 1.0)),

  /// @brief Couleur de fond spéciale
  specialBackgroundColor(color: Color.fromRGBO(5, 195, 115, 1.0)),

  /// @brief Couleur du texte sur "specialBackgroundColor"
  specialText(color: Color.fromRGBO(255, 255, 255, 1)),

  /// @brief Couleur de fond pouvant aller sur "backgroundColor"
  upperBackgroundColor(color: Color.fromRGBO(40, 40, 51, 1.0)),

  /// @brief Couleur du texte sur "upperBackgroundColor"
  upperText(color: Color.fromRGBO(255, 255, 255, 1));

  const AppTheme({required this.color});

  final Color color;
}
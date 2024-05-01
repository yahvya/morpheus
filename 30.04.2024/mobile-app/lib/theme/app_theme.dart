import 'dart:ui';

import 'package:flutter/material.dart';

/// @brief Thème couleur de l'application
enum AppTheme{
  /// @brief Couleur de fond de l'application
  backgroundColor(color: Color.fromRGBO(255, 255, 255, 1.0)),
  /// @brief Couleur du texte sur "backgroundColor"
  textColor(color: Color.fromRGBO(0, 0, 0, 1)),
  // /// @brief Couleur de fond spéciale
  specialBackgroundColor(color: Color.fromRGBO(31, 31, 60, 1.0)),
  // /// @brief Couleur du texte sur "specialBackgroundColor"
  specialText(color: Color.fromRGBO(255, 255, 255, 1));
  // /// @brief Couleur de fond pouvant aller sur "backgroundColor"
  // upperBackgroundColor(color: ),
  // /// @brief Couleur du texte sur "upperBackgroundColor"
  // upperText(color: );

  const AppTheme({required this.color});

  final Color color;
}
import 'package:flutter/material.dart';
import 'package:mobileapp/theme/app_theme.dart';

/// @brief Model de page de l'application
abstract class PageModel{
  const PageModel();

  /// @brief Construis le modèle de page
  /// @return La page construire
  static buildPage(pageContent){
    return Scaffold(
      body: pageContent,
      backgroundColor: AppTheme.backgroundColor.color,
    );
  }

  /// @brief Formate un format de texte stylisé par défaut
  /// @param text le texte
  /// @param center si le texte doit être centré
  /// @return le Composant text
  static specialText({required String text,bool center = true}){
    return Text(
      text,
      softWrap: true,
      textAlign: center ? TextAlign.center : null,
      style: const TextStyle(
        fontSize: 25,
        fontFamily: "Poppins",
        fontWeight: FontWeight.w600,
      ),
    );
  }

  /// @brief Formate un format de texte stylisé par défaut
  /// @param text le texte
  /// @param center si le texte doit être centré
  /// @return le Composant text
  static basicText({required String text,bool center = true}){
    return Text(
      text,
      softWrap: true,
      textAlign: center ? TextAlign.center : null,
      style: const TextStyle(
        fontSize: 20,
        fontFamily: "OpenSans",
        fontWeight: FontWeight.w500,
      ),
    );
  }
}
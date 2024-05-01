import 'package:flutter/material.dart';
import 'package:mobileapp/theme/app_theme.dart';

/// @brief Model de page de l'application
abstract class PageModel{
  const PageModel();

  /// @brief Construis le modèle de page
  /// @param pageContent contenu de la page
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
  /// @param size taille de la police
  /// @param color Couleur à mettre
  /// @return le Composant text
  static specialText({required String text,bool center = true,double size = 30,Color? color}){
    return Text(
      text,
      softWrap: true,
      textAlign: center ? TextAlign.center : null,
      style: TextStyle(
        fontSize: size,
        fontFamily: "Poppins",
        fontWeight: FontWeight.w600,
        color: color ?? AppTheme.textColor.color
      ),
    );
  }

  /// @brief Formate un format de texte stylisé par défaut
  /// @param text le texte
  /// @param center si le texte doit être centré
  /// @param size taille de la police
  /// @param color Couleur à mettre
  /// @return le Composant text
  static basicText({required String text,bool center = true,double size = 19,Color? color}){
    return Text(
      text,
      softWrap: true,
      textAlign: center ? TextAlign.center : null,
      style: TextStyle(
        fontSize: size,
        fontFamily: "OpenSans",
        fontWeight: FontWeight.w500,
        color: color ?? AppTheme.textColor.color
      ),
    );
  }
}
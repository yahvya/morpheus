import 'package:flutter/material.dart';
import 'package:mobileapp/theme/app_theme.dart';

/// @brief Model de page de l'application
abstract class PageModel extends StatelessWidget{
  /// @brief Construis le modèle de page
  /// @return La page construire
  buildPage(Column pageContent){
    return Scaffold(
      body: SingleChildScrollView(
        child: pageContent,
      ),
      backgroundColor: AppTheme.backgroundColor.color,
    );
  }

  /// @brief Formate un format de texte stylisé par défaut
  /// @return le Composant text
  static specialText({required String text}){
    return Text(
      text,
      style: TextStyle(
        fontSize: 25,
        fontFamily: "Poppins",
        fontWeight: FontWeight.w600,
      ),
    );
  }

  /// @brief Formate un format de texte stylisé par défaut
  /// @return le Composant text
  static basicText({required String text}){
    return Text(
      text,
      style: TextStyle(
        fontSize: 20,
        fontFamily: "OpenSans",
        fontWeight: FontWeight.w500
      ),
    );
  }
}
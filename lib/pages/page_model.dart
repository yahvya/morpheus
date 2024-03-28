import 'package:flutter/material.dart';
import 'package:morpheus_team/assets/image_assets.dart';

import '../style-config/app_theme.dart';

/// @brief modèle de page
abstract class PageModel{
  /// @brief Construis le modèle de page
  /// @param pageContent contenu du la page
  /// @return la page construite
  static Widget buildFrom(Widget pageContent){
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            const SizedBox(height: 30,),
            Align(
                alignment: Alignment.topRight,
                child: Container(
                  padding: const EdgeInsets.all(15),
                  child: ImageAssets.favicon.image(width: 60,height: 55),
                )
            ),
            const SizedBox(height: 30,),
            pageContent
          ],
        )
      ),
      backgroundColor: AppTheme.background
    );
  }

  /// @brief Construis le titre de la page
  /// @return le titre formaté en widget
  static Widget pageTitle(String title){
    return Column(
      children: [
        Text(
          title.toUpperCase(),
          style: const TextStyle(
              fontWeight: FontWeight.bold,
              color: AppTheme.textOnBackground,
              fontSize: 21
          ),
          textAlign: TextAlign.center,
          softWrap: true,
        ),
        const SizedBox(
          height: 40
        )
      ]
    );
  }
}

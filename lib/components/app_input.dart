import 'package:flutter/material.dart';
import 'package:morpheus_team/style-config/app_theme.dart';

/// @brief Input de l'application
class AppInput extends StatelessWidget{
  const AppInput({super.key,required this.placeholder,this.isProtected = false,this.onChanged});

  /// @brief Texte affiché en placeholder
  @protected
  final String placeholder;

  /// @brief Si le champs est un champs protégé
  final bool isProtected;

  /// @brief Conteneur de la chaine saisie dans le input
  final void Function(String)? onChanged;

  @override
  Widget build(BuildContext context){
    OutlineInputBorder bordersStyle = OutlineInputBorder(
        borderSide: const BorderSide(
            color: AppTheme.onBackgroundLightText
        ),
        borderRadius: BorderRadius.circular(4)
    );

    return Center(
      child: FractionallySizedBox(
        widthFactor: 0.9,
        child: TextFormField(
          onChanged: onChanged,
          obscureText: isProtected,
          decoration: InputDecoration(
            labelText: placeholder,
            labelStyle: const TextStyle(
                color: AppTheme.onBackgroundLightText
            ),
            floatingLabelStyle: const TextStyle(
                color: AppTheme.onBackgroundLightText
            ),
            fillColor: AppTheme.onBackground,
            filled: true,
            border: bordersStyle,
            focusedBorder: bordersStyle,
            enabledBorder: bordersStyle
          ),
          style: const TextStyle(
              color: AppTheme.onBackgroundText
          ),
          cursorColor: AppTheme.special,
        )
      )
    );
  }
}

import 'package:flutter/material.dart';
import 'package:mobileapp/theme/app_theme.dart';

/// @brief Champs de saisie
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
      borderSide: BorderSide(
        color: AppTheme.specialBackgroundColor.color
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
                  labelStyle: TextStyle(
                    color: AppTheme.upperText.color
                  ),
                  floatingLabelStyle: TextStyle(
                    color: AppTheme.upperText.color
                  ),
                  fillColor: AppTheme.upperBackgroundColor.color,
                  filled: true,
                  border: bordersStyle,
                  focusedBorder: bordersStyle,
                  enabledBorder: bordersStyle
              ),
              style: TextStyle(
                  color: AppTheme.upperText.color
              ),
              cursorColor: AppTheme.specialBackgroundColor.color,
            )
        )
    );
  }
}
import 'package:flutter/material.dart';
import 'package:morpheus_team/style-config/app_theme.dart';

/// @brief Bouton de l'application
class AppButton extends StatelessWidget{
  const AppButton({super.key,required this.containedText,this.onPressed});

  /// @brief Texte du bouton
  @protected
  final String containedText;

  /// @brief action à l'appui du boutton
  @protected
  final void Function()? onPressed;

  @override
  Widget build(BuildContext context){
    return TextButton(
        onPressed: onPressed,
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all(AppTheme.special),
          shape: MaterialStateProperty.all(const RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(4) )
          )),
          padding: MaterialStateProperty.all(const EdgeInsets.all(20))
        ),
        child: Text(
          containedText,
          style: const TextStyle(
            color: AppTheme.textOnSpecial,
            fontSize: 17
          ),
        ),
    );
  }
}

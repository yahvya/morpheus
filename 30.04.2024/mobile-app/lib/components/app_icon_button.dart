import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobileapp/theme/app_theme.dart';

/// @brief Bouton d'icône
class AppIconButton extends StatelessWidget{
  const AppIconButton({super.key,required this.icon,this.onClick});

  /// @brief Icône du bouton
  final IconData icon;

  /// @brief Action à exécuter au click sur le bouton
  final void Function()? onClick;

  @override
  build(BuildContext context){
    var upperColorState = MaterialStateProperty.all(AppTheme.specialText.color);

    return IconButton(
      onPressed: onClick,
      icon: Icon(icon),
      color: AppTheme.specialText.color,
      style: ButtonStyle(
        padding: MaterialStateProperty.all(const EdgeInsets.all(5)),
        shape: MaterialStateProperty.all(const RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(3))
        )),
        backgroundColor: MaterialStateProperty.all(AppTheme.specialBackgroundColor.color),
        foregroundColor: upperColorState,
      ),
    );
  }
}
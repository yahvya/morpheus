import 'package:flutter/material.dart';
import 'package:morpheus/config/ThemeConfig.dart';

/// bouton de l'application
class AppButton extends StatelessWidget{
  const AppButton({super.key,required this.text, this.onPressed});

  final String text;
  final void Function()? onPressed;

  @override
  Widget build(BuildContext context){
    return TextButton(
        onPressed: onPressed,
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all(ThemeConfig.specialColor),
          shape: MaterialStateProperty.all(
            const RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(4))
            )
          )
        ),
        child: Text(
          text,
          style: TextStyle(
              color: ThemeConfig.specialTextColor
          )
        ),
    );
  }
}

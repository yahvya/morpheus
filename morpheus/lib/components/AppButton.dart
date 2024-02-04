import 'package:flutter/cupertino.dart';

/// boutton de l'application
class AppButton extends StatelessWidget{
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context){
    return TextButton(
      onPressed: onPressed,
      child: Text("Lancer L'application"),
    );
  }
}
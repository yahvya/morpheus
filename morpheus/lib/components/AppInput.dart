import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';


class AppInput extends StatelessWidget{
  const AppInput({super.key,required this.label,required this.placeholder,this.isProtected = false});

  final String label;
  final String placeholder;
  final bool isProtected;

  @override
  Widget build(BuildContext context){
    var colorScheme = Theme.of(context).colorScheme;
    var textColor = colorScheme.onSurface;
    var opacityColor = textColor.withOpacity(0.4);

    return Container(
      padding: const EdgeInsets.fromLTRB(10, 0,10, 0),
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.all(Radius.circular(4)),
        border: Border.all(color: Color(0xFFD0D2CF)),
        color: Color(0xFF1B1B1B)
      ),
      child: TextFormField(
        cursorColor: textColor,
        obscureText: isProtected,
        decoration: InputDecoration(
          border: InputBorder.none,
          hintText: placeholder,
          hintStyle: TextStyle(
            fontSize: 15,
            color: textColor
          ),
          labelText: label,
          labelStyle: TextStyle(
            fontSize: 20,
            color: opacityColor
          ),
          floatingLabelStyle: TextStyle(
            color: opacityColor.withOpacity(0.4)
          ),
          floatingLabelBehavior:FloatingLabelBehavior.always
        ),
      )
    );
  }
}
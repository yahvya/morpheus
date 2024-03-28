import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:morpheus/config/ThemeConfig.dart';


class AppInput extends StatelessWidget{
  const AppInput({super.key,required this.label,required this.placeholder,this.isProtected = false});

  final String label;
  final String placeholder;
  final bool isProtected;

  @override
  Widget build(BuildContext context){
    var opacityColor = ThemeConfig.bodyUpTextColor.withOpacity(0.7);

    return Container(
      padding: const EdgeInsets.fromLTRB(10, 0,10, 0),
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.all(Radius.circular(4)),
        border: Border.all(color: ThemeConfig.backgroundTextColor),
        color: ThemeConfig.bodyUpBackground
      ),
      child: TextFormField(
        cursorColor: ThemeConfig.bodyUpTextColor,
        obscureText: isProtected,
        style: TextStyle(color: ThemeConfig.bodyUpTextColor),
        decoration: InputDecoration(
          border: InputBorder.none,
          hintText: placeholder,
          hintStyle: TextStyle(
            fontSize: 15,
            color: ThemeConfig.bodyUpTextColor
          ),
          labelText: label,
          labelStyle: TextStyle(
            fontSize: 20,
            color: opacityColor
          ),
          floatingLabelStyle: TextStyle(
            color: opacityColor
          ),
          floatingLabelBehavior:FloatingLabelBehavior.always
        ),
      )
    );
  }
}
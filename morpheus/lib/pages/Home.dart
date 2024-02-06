import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:morpheus/components/AppInput.dart';

/// page d'accueil du projet
class Home extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return Scaffold(
      backgroundColor: Colors.white,
      body: Container(
        color: Color(0xFF1B1B1B),
        child: AppInput(),
      )
    );
  }
}

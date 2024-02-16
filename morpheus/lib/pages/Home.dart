import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:morpheus/components/AppInput.dart';

/// page d'accueil du projet
class Home extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return Scaffold(
      backgroundColor: Color(0XFF1E1E1E),
      body: Container(
        child: Column(
          children: [
            SizedBox(
              height: 50,
            ),
            AppInput(label: "Email",placeholder: "entrez votre email",)
          ],
        ),
      )
    );
  }
}

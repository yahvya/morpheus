import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

/// zone de saisie de l'application
class AppInput extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return Column(
      children: [
        SizedBox(height: 16),
        TextField(
          cursorColor: Color(0xFFFDFDFD),
          style: TextStyle(
            color: Color(0xFFFDFDFD)
          ),
          decoration: InputDecoration(
            focusColor: Color(0xFFFDFDFD),
            hoverColor: Color(0xFFFDFDFD),
            labelText: 'Entrez votre email', // Libellé du champ de saisie
            border: OutlineInputBorder(), // Bordure du champ
          ),
        ),
        SizedBox(height: 16), // Espacement entre les champs
        TextField(
          cursorColor: Color(0xFFFDFDFD),
          style: TextStyle(
              color: Color(0xFFFDFDFD)
          ),
          obscureText: true, // Pour masquer les caractères du mot de passe
          decoration: InputDecoration(
            focusColor: Color(0xFFFDFDFD),
            hoverColor: Color(0xFFFDFDFD),
            labelText: 'Entrez votre mot de passe', // Libellé du champ de saisie
            border: OutlineInputBorder(), // Bordure du champ
          ),
        ),
      ],
    );
} 
}
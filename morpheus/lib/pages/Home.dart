import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:morpheus/components/AppInput.dart';
import 'package:morpheus/components/VideoRecapZone.dart';
import 'package:morpheus/config/ThemeConfig.dart';

/// page d'accueil du projet
class Home extends StatelessWidget{
  @override
  Widget build(BuildContext context){
    return Scaffold(
      backgroundColor: ThemeConfig.backgroundColor,
      body: Container(
        child: Column(
          children: [
            SizedBox(
              height: 50,
            ),
            AppInput(label: "Email",placeholder: "entrez votre email",),
            VideoRecapZone(name: "Recap de test", videoPath: "assets/video.mp4")
          ],
        ),
      )
    );
  }
}

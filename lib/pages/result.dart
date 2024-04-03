import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:morpheus_team/pages/page_model.dart';
import '../assets/image_assets.dart';
import '../style-config/app_theme.dart';

class Result extends StatelessWidget {
   Result({super.key});

  final List<Map<String, dynamic>> testDatas = [
    {
      "section": "Distances",
      "content": [
        {
          "title": "obm",
          "value": "10 cm"
        },
        {
          "title": "obm",
          "value": "5 cm"
        }
      ]
    },
    {
      "content": [
        {
          "title": "obm 2",
          "value": "20 cm"
        },
        {
          "title": "obm 2",
          "value": "15 cm"
        }
      ]
    }
  ];

  @override
  Widget build(BuildContext context){
    // configuration de style
    const headTitleStyle = TextStyle(
        color: AppTheme.textOnBackground,
        fontSize: 30
    );

    const basicStyle = TextStyle(
        color: AppTheme.textOnBackground,
        fontSize: 20
    );

    const separator = SizedBox(height: 10,);

    var sections = [];

    for(var config in testDatas){
      sections.add(
        Text(
          config["section"],
          style: headTitleStyle
        )
      );
      for(var sectionContent in config["content"]){
          sections.add(
            Text(
              "${sectionContent["title"]} - ${sectionContent["value"]}",
              style: headTitleStyle
            )
          );
      }
    }

    return PageModel.buildFrom(
      Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Outils
            const Text(
              "Outils Adéquat",
              style: headTitleStyle,
            ),
            const SizedBox(height: 10,),
            // image outils
            ImageAssets.outils.image(width: 100, height: 100),
            const SizedBox(height: 70,),
            // Mallampati
            const Text(
              "Mallampati",
              style: headTitleStyle
            ),
            const SizedBox(height: 10,),
            // image mallampati
            ImageAssets.mallampati.image(width: 100, height: 100),
            const SizedBox(height: 70,),
            // affichage des sections
            ...sections
          ]
      )
    );
  }
}
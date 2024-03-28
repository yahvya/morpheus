import 'package:flutter/material.dart';
import 'package:morpheus_team/assets/image_assets.dart';
import 'package:morpheus_team/components/app_button.dart';
import 'package:morpheus_team/pages/page_model.dart';
import 'package:morpheus_team/pages/record.dart';
import '../components/tutorial_step.dart';

/// @brief Page d'accueil
class Home extends StatelessWidget{
  const Home({super.key});

  @override
  Widget build(BuildContext context){
    return PageModel.buildFrom(Column(
      children: [
        TutorialStep(
          stepCount: 1,
          image: ImageAssets.tap.image(width: 60,height: 60),
          description: "Appuyez sur le bouton de lancement"
        ),
        const SizedBox(height: 30),
        TutorialStep(
          stepCount: 2,
          image: ImageAssets.rec.image(width: 60,height: 60),
          description: "Suivez les différentes étapes"
        ),
        const SizedBox(height: 80,),
        AppButton(
          containedText: "Lancer un enregistrement",
          onPressed: (){
            Navigator.of(context).push(MaterialPageRoute(builder: (context) => const Record()));
          },
        )
      ]
    ));
  }
}

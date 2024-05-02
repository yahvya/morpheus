import 'package:flutter/material.dart';
import 'package:mobileapp/app/api/api_result.dart';
import 'package:mobileapp/app/profiles/profile.dart';
import 'package:mobileapp/components/app_button.dart';
import 'package:mobileapp/components/app_message.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/pages/profile_page.dart';
import 'package:video_player/video_player.dart';

/// @brief Page d'affichage de résultat de traitement
class ResultPage extends StatefulWidget{
  const ResultPage({super.key,required this.profiles,required this.result});

  /// @brief Résultat de traitement
  final ApiResult result;

  /// @brief Liste des profiles
  final List<Profile> profiles;
  
  @override
  State<StatefulWidget> createState() {
    return ResultPageState();
  }
}

/// @brief Etat de la page d'affichage de résultat de traitement
class ResultPageState extends State<ResultPage>{
  VideoPlayerController controller = VideoPlayerController.networkUrl(
    Uri.parse("https://www.ebooksgratuits.com/temp/mp4/Choeurs_sur_Seine_chante_l_Europe_-_01_-_Poulenc_-_La_petite_fille_sage.mp4"),
  );

  ResultPageState(){
    controller.initialize().then((_){
      controller.setLooping(true);
      controller.play();
    });
  }

  @override
  void dispose() {
    controller.dispose();
    
    super.dispose();
  }

  @override
  Widget build(BuildContext context){
    return PageModel.buildPage(SingleChildScrollView(
      child: SafeArea(
        child: Column(
        children: [
          const SizedBox(height: 30),
          PageModel.specialText(text: "Résultats des traitements".toUpperCase()),
          const SizedBox(height: 60),
          SizedBox(
            height: 250,
            width: 250,
            child: VideoPlayer(controller)
          ),
          const SizedBox(height: 40),
          PageModel.specialText(
            text: "Données",
            size: 24
          ),
          const SizedBox(height: 20),
          buildResultDatas(),
          const SizedBox(height: 60),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              AppButton(
                text: "Retour",
                icon: Icons.arrow_back,
                onPressed: (){
                  Navigator.of(context).pushReplacement(MaterialPageRoute(
                    builder: (BuildContext context) => ProfilePage(profiles: widget.profiles)
                  ));
                },
              ),
              const SizedBox(width: 30,),
              AppButton(
                text: "Télécharger", 
                icon: Icons.download_rounded,
                onPressed: () => widget.result.downloadAsZip(),
              ),
            ],
          ),
          const SizedBox(height: 80,)
        ],
      ),
      )
    ));
  }
  
  /// @brief construis l'affichage des données du résultats
  /// @return l'afficheur 
  Column buildResultDatas(){
    const spacing = SizedBox(height: 20);
    List<Widget> children = [];

    // création d'affichage des données
    widget.result.textualsDatas.forEach((key, value) { 
      children.addAll([
        AppMessage(message: "$key: $value"),
        spacing
      ]);
    });

    return Column(
      children: children,
    );
  }
}
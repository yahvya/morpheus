import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:mobileapp/app/api/api_result.dart';
import 'package:mobileapp/app/api/contact.dart';
import 'package:mobileapp/app/profiles/profile.dart';
import 'package:mobileapp/app/record/record_check.dart';
import 'package:mobileapp/app/record/record_manager.dart';
import 'package:mobileapp/app/utils/json_assets_reader.dart';
import 'package:mobileapp/components/app_text_button.dart';
import 'package:mobileapp/config/assets_config.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/pages/result_page.dart';
import 'package:mobileapp/theme/app_theme.dart';
import 'package:video_player/video_player.dart';

/// @brief Page d'enregistrement
class RecordPage extends StatefulWidget{
  const RecordPage({super.key,required this.profiles,required this.usedProfile});

  /// @brief Profil de l'utilisateur entrain d'enregistrer
  final Profile usedProfile;

  /// @brief Liste des profiles
  final List<Profile> profiles;

  @override
  State<StatefulWidget> createState() {
    return RecordPageState();
  }
}

/// @brief Etat de la page d'enregistrement
class RecordPageState extends State<RecordPage>{
  /// @brief score actuel de mallampati
  int currentMallampati = 1;

  /// @brief Range min de mallampati
  int mallampatiMin = 1;

  /// @brief Range min de mallampati
  int mallampatiMax = 4;

  /// @brief Durée de la vidéo en secondes
  late int videoDuration;

  /// @brief Gestionnaire d'enregistrement
  RecordManager recordManager = RecordManager();

  /// @brief Gestionnaire de l'affichage vidéo
  VideoPlayerController? playerController;

  /// @brief Lecteur vidéo
  VideoPlayer? player;

  /// @brief Si une validation est en cours
  bool isValidating = false;

  /// @brief Si une détection est en cours
  bool isDetecting = false;

  /// @brief Message d'erreur en cas de non validation
  String? errorMessage;

  /// @brief Vérificateur
  RecordCheck checker = RecordCheck();

  RecordPageState(){
    // chargement du range de mallampati et de la durée de la vidéo
    JsonAssetsReader.get(toRead: AssetsConfig.apiConfig).then((config){
      var apiConfig = config as Map<String,dynamic>;
      var mallampatiConfig = apiConfig["mallampati"] as Map<String,dynamic>;

      setState((){
        mallampatiMin = mallampatiConfig["min"] as int;
        mallampatiMax = mallampatiConfig["max"] as int;
        videoDuration = apiConfig["video-duration"] as int;
      });
    });

    // chargement de la caméra
    loadCameras();
  }

  /// @brief Tente de charger la caméra
  void loadCameras() async{
    try{
      var foundedCameras = await availableCameras();

      // recherche de la caméra arrière
      for(var f in foundedCameras){
        if(f.lensDirection == CameraLensDirection.back){
          var cameraController = CameraController(
            f,
            ResolutionPreset.max,
            enableAudio: false
          );

          await cameraController.initialize();

          setState((){
            recordManager.setController(controller: cameraController);
          });

          return;
        }
      }
    }
    catch(_){}
  }

  @override
  build(BuildContext context){
    return PageModel.buildPage(SingleChildScrollView(
      child: SafeArea(child: Center(
        child: Stack(
          children: [
            Column(
              children: [
                const SizedBox(height: 30),
                PageModel.specialText(text: "Enregistrement".toUpperCase()),
                const SizedBox(height: 60),
                  if(errorMessage != null)
                    PageModel.basicText(text: errorMessage!,size: 16),
                const SizedBox(height: 10),
                buildCameraZone(context: context),
                const SizedBox(height: 40),
                buildSlider(context: context),
                const SizedBox(height: 30),
                PageModel.basicText(
                  text: "Assurez vous d'avoir fourni toutes les informations",
                  size: 13
                ),
                const SizedBox(height: 10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    AppTextButton(
                      text: "Annuler",
                      onClick: () => returnToProfiles(context: context),
                    ),
                    const SizedBox(width: 35),
                    AppTextButton(
                      text: "Valider",
                      onClick: () => sendDatas(context: context),
                    ),
                  ],
                ),
                const SizedBox(height: 80)
              ],
            )
            ,
            if(isValidating)
              buildWaitingScreen()
          ],
        ),
      )),
    ));
  }

  @override
  void dispose() {
    if(recordManager.isRecording){
      recordManager.stopRecord();
    }

    if(playerController != null){
      playerController!.dispose();
    }

    super.dispose();
  }

  /// @brief Construis la zone de récupération des informations du slider
  /// @param context le contexte
  /// @return la zone du slider
  Column buildSlider({required BuildContext context}){
    return Column(
      children: [
        PageModel.specialText(
          text: "Score de mallampati : $currentMallampati",
          size: 20
        ),
        const SizedBox(height: 20),
        Slider(
          value: currentMallampati.toDouble(),
          onChanged: (double newValue){
            // blocage de l'action en cas de vidéo en cours ou de validation
            if(recordManager.isRecording || isValidating){
              return;
            }

            setState(() {
              currentMallampati = newValue.toInt();
            });
          },
          min: mallampatiMin.toDouble(),
          max: mallampatiMax.toDouble(),
          activeColor: AppTheme.specialBackgroundColor.color,
          inactiveColor: AppTheme.specialBackgroundColor.color,
          secondaryActiveColor: AppTheme.specialBackgroundColor.color,
          thumbColor: AppTheme.specialText.color,
          mouseCursor: MouseCursor.uncontrolled,
          divisions: mallampatiMax - mallampatiMin,
          label: currentMallampati.toString()
        )
      ],
    );
  }

  /// @brief Construis la zone caméra
  /// @param context le context
  /// @return la zone construite
  Column buildCameraZone({required BuildContext context}){
    List<Widget> children = [];

    // définition du titre
    if(recordManager.camera != null && recordManager.isRecording){
      children.add(
        PageModel.specialText(
          text: "En cours d'enregistrement : ${recordManager.registeredDuration} sec",
          size: 20,
        )
      );
    }
    else if(recordManager.getLastRecordedVideo() != null){
      children.add(
          PageModel.specialText(
            text: "Validation",
            size: 20,
          )
      );
    }
    else{
      children.add(
        PageModel.specialText(
          text: "Appuyez pour enregistrer",
          size: 20,
        )
      );
    }

    children.add(const SizedBox(height: 30));

    // affichage caméra ou recap
    if(recordManager.camera != null){
      var size = MediaQuery.of(context).size;
      var width = size.width * 0.9;
      var height = size.height * 0.7;

      if(recordManager.getLastRecordedVideo() == null){
        children.add(Stack(
          children: [
            Container(
              width: width,
              height: height,
              decoration: BoxDecoration(
                  border: getRecordBorder()
              ),
              child: recordManager.preview,
            ),
            if(!recordManager.isRecording)
              Container(
                  width: width,
                  height: height,
                  color: AppTheme.specialBackgroundColor.color.withOpacity(0.6),
                  child: IconButton(
                    icon: const Icon(Icons.photo_camera),
                    onPressed: () => startRecord(),
                  )
              )
          ],
        )
        );
      }
      else{
        var player = createPlayerFromRecord();

        if(player != null){
          children.add(player);
        }
      }
    }
    else{
      children.add(
        PageModel.basicText(text: "Caméra en cours de chargement, veuillez patienter",size: 16)
      );
    }

    return Column(
      children: children,
    );
  }

  /// @brief Ecran de chargement
  Positioned buildWaitingScreen(){
    return Positioned.fill(
      child: Container(
        color: AppTheme.backgroundColor.color.withOpacity(0.8),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            PageModel.specialText(
              text: "Traitement des données ...",
              size: 22
            ),
            const SizedBox(
              height: 40,
            ),
            SizedBox(
              width: 60,
              height: 60,
              child: CircularProgressIndicator(
                backgroundColor: AppTheme.backgroundColor.color,
                color: AppTheme.specialBackgroundColor.color,
              ),
            )
          ],
        )
      )
    );
  }

  /// @brief Démarre l'enregistrement
  void startRecord(){
    recordManager.startRecord(
      toDoOnTimerIncrement: (){
        if(recordManager.registeredDuration > videoDuration){
          recordManager.stopRecord().then((_){
            setState(() {
              isDetecting = false;
            });
          });
        }
        else{
          setState(() {});
        }
      },
      imageManager: (CameraImage frame){
        if(!recordManager.isRecording || isDetecting){
          return;
        }
        
        isDetecting = true;

        // vérification de la frame
        checker.check(camera: recordManager.camera!,frame: frame).then((success){
          isDetecting = false;

          if(!success && !recordManager.isInPause){
            recordManager.pauseRecord();
            
            // mise à jour de l'état pour le changement de bordure
            setState(() {});
          }
          else if(success && recordManager.isInPause){
            recordManager.resumeRecord();

            // mise à jour de l'état pour le changement de bordure
            setState(() {});
          }
        });
      }
    );
  }

  /// @brief Crée la bordure en fonction du mode d'enregistrement
  Border getRecordBorder(){
    Color boxColor;

    if(recordManager.isRecording){
      // si est en pause alors bloqué
      if(recordManager.isInPause){
        boxColor = Colors.red;
      }
      else{
        boxColor = Colors.green;
      }
    }
    else{
      boxColor = Colors.transparent;
    }

    return Border.all(color: boxColor);
  }

  /// @brief Crée le player à partir de l'enregistrement fait
  /// @return le player
  SizedBox? createPlayerFromRecord(){
    try{
      if(playerController != null){
        playerController!.dispose();
      }

      playerController = VideoPlayerController.file(
        File(recordManager.getLastRecordedVideo()!.path)
      );

      playerController!.initialize().then((_){
        playerController!.setLooping(true);
        playerController!.play();
      });

      return SizedBox(
        width: 200,
        height: 200,
        child:  VideoPlayer(playerController!)
      );
    }
    catch(_){
      return null;
    }
  }

  /// @brief Retourne sur la page profiles
  /// @param context contexte de création
  void returnToProfiles({required BuildContext context}){
    Navigator.pop(context);
  }

  /// @brief Démarre l'envoi
  /// @param context de création
  void sendDatas({required BuildContext context}){
    setState(() {
      isValidating = true;
    });
    Contact.contact(
      senderProfile: widget.usedProfile,
      video: recordManager.getLastRecordedVideo()!, 
      mallampatiScore: currentMallampati,
      usedCamera: recordManager.camera!
      ).then((ApiResult result){
      // erreur d'appel ajout du message
      if(!result.successfulyCalled){
        setState(() {
          errorMessage = result.errorMessage;
          isValidating = false;
        });
        return;
      }
      
      // affichage de la page résultat
      Navigator.of(context).pushReplacement(MaterialPageRoute(
        builder: (BuildContext context) => ResultPage(result: result,profiles: widget.profiles,)
      ));
    });
  }
}
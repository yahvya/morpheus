import 'dart:async';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:morpheus_team/app/detection/detection_config.dart';
import 'package:morpheus_team/components/app_button.dart';
import 'package:morpheus_team/pages/page_model.dart';
import 'package:morpheus_team/style-config/app_theme.dart';
import 'package:video_thumbnail/video_thumbnail.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';
import 'package:crypto/crypto.dart';

import 'home.dart';

/// @brief Page d'enregistrement des sections vidéos
class Record extends StatefulWidget{
  const Record({super.key});

  @override
  State<StatefulWidget> createState() {
    return RecordState();
  }
}

class RecordState extends State<Record>{
  /// @brief sections restantes
  late List<Map<String, Object?>> toDo;

  /// @brief Sections déjà prises
  List<Map<String, Object?>> alreadyDone = [];

  /// @brief Chemins de video
  List<String> videoPaths = [];

  /// @brief Timer
  Timer? timer;

  /// @brief Temps en secondes restant
  late int timerSeconds;

  /// score actuel de mallampati
  late int currentMallampati;

  /// @brief Si l'enregistrement de la section actuelle a démarré
  bool startedRecordingCurrentSection = false;

  /// @brief Controller vidéo
  CameraController? controller;

  @override
  void initState() {
    super.initState();

    // copie de la liste des sections à prendre
    toDo = List.from(DetectionManager.config);
    timerSeconds = toDo[0].cast()["duration"];
    currentMallampati = DetectionManager.mallampatiRange.first;

    // lancement du chargement des caméras
    loadCamera();
  }

  @override
  void dispose() {
    super.dispose();

    if(controller != null) {
      controller!.dispose();
    }

    for (var config in alreadyDone) {
      config.cast()["preview"].dispose();
    }
  }

  @override
  Widget build(BuildContext context) {
    // liste des éléments traités
    var alreadyDoneView = ListView.separated(
      itemBuilder: (BuildContext ctx,int index){
        var datas = alreadyDone[index].cast();

        return GestureDetector(
          // évènement de reprise de cette section
          onTap: (){
            // blocage si un record en cours
            if(startedRecordingCurrentSection) {
              return;
            }

            setState((){
              // suppression dans les éléments déjà fait
              alreadyDone.removeAt(index);

              // suppression des données ajoutées
              datas.remove("preview");
              datas.remove("video");

              // remise dans les action à faire
              toDo.insert(0,datas.cast());
            });
          },
          child: Column(
            children: [
              SizedBox(
                width: 130,
                height: 130,
                child: datas["preview"],
              ),
              const SizedBox(height: 10),
              Text(
                datas["text"],
                style: const TextStyle(
                    color: AppTheme.lightTextOnBackground,
                    fontSize: 18
                ),
              )
            ],
          ),
        );
      },
      separatorBuilder: (BuildContext ctx,int index) => const SizedBox(width: 30,),
      itemCount: alreadyDone.length,
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.all(20),
    );

    // descriptions de l'élément actuel
    List<Widget> instructions = [];

    Widget upperZone;

    // si chaque section est enregistré
    if(toDo.isEmpty){
      upperZone = Column(
        children: [
          AppButton(
            containedText: "Lancer le traitement",
            onPressed: () { sendVideos(
              'http://10.0.2.2:8000/video',
              videoPaths,
            ); },
          ),
          // choix du score de mallampati
          const SizedBox(height: 45),
          const Text(
            "Veuillez choisir le score de mallampati",
            style: TextStyle(
              color: AppTheme.textOnBackground,
              fontSize: 24
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 17),
          Slider(
            value: currentMallampati.toDouble(),
            onChanged: (double newValue){
              setState(() {
                currentMallampati = newValue.toInt();
              });
            },
            min: DetectionManager.mallampatiRange.first.toDouble(),
            max: DetectionManager.mallampatiRange.last.toDouble(),
            activeColor: AppTheme.special,
            inactiveColor: AppTheme.special,
            secondaryActiveColor: AppTheme.special,
            thumbColor: AppTheme.textOnSpecial,
            mouseCursor: MouseCursor.uncontrolled,
            divisions: DetectionManager.mallampatiRange.last - DetectionManager.mallampatiRange.first,
            label: currentMallampati.toString()
          ),
          const SizedBox(height: 13),
          Text(
            currentMallampati.toString(),
            style: const TextStyle(
              color: AppTheme.textOnBackground,
              fontSize: 20
            )
          )
        ],
      );
    }
    else{
      Map<String,Object?> currentSection = toDo[0];

      // ajout de la zone d'enregistrement
      upperZone =  Column(
        children: [
          // secondes restantes
          Text(
              "$timerSeconds sec",
              style: const TextStyle(
                  color: AppTheme.special,
                  fontSize: 20,
                  fontWeight: FontWeight.bold
              )
          ),
          const SizedBox(height: 15),

          // retour caméra
          Stack(
            children: [
              Container(
                  width: 200,
                  height: 300,
                  color: AppTheme.onBackground,
                  child: controller == null ? null : CameraPreview(controller!)
              ),
              if(!startedRecordingCurrentSection)
                Container(
                  width: 200,
                  height: 300,
                  color: AppTheme.onBackground.withOpacity(0.6),
                  child: IconButton(
                    icon: const Icon(Icons.photo_camera),
                    onPressed: () { startRecord(); },
                  )
                )
            ],
          ),
          const SizedBox(height: 15),

          // titre de la section filmé
          Text(
            currentSection.cast()["text"],
            style: const TextStyle(
                color: AppTheme.textOnBackground,
                fontSize: 20
            ),
          )
        ],
      );

      // ajout des instructions
      for(var instruction in currentSection.cast()["instructions"]){
        instructions.addAll([
          Text(
            "- $instruction",
            style: const TextStyle(
                color: AppTheme.lightTextOnBackground,
                fontSize: 15
            ),
          ),
          const SizedBox(height: 20)
        ]);
      }
    }

    return PageModel.buildFrom(Column(
      children: [
        // titre de la page
        PageModel.pageTitle("Enregistrement des informations"),

        // zone de retour vidéo caméra ou validation
        upperZone,
        const SizedBox(height: 40,),

        // affichage des descriptions
        Column(children: instructions),
        const SizedBox(height: 30),

        // récapitulatif des sections déjà prises
        SizedBox(
          height: alreadyDone.isEmpty ? 0 : 250,
          child: alreadyDoneView,
        ),

        // annulation de l'action
        AppButton(
          containedText: "Annuler",
          onPressed: (){
            Navigator.of(context).push(MaterialPageRoute(builder: (context) => const Home()));
          },
        ),
        const SizedBox(height: 70),
      ],
    ));
  }

  /// @brief Charge la caméra arrière
  @protected
  void loadCamera() async{
    try{
      var camerasDescriptions = await availableCameras();
      var backCamera = camerasDescriptions.firstWhere((cameraDescription) => cameraDescription.lensDirection == CameraLensDirection.back);

      controller = CameraController(backCamera, ResolutionPreset.max,enableAudio: false);

      await controller!.initialize();

      setState(() {});
    }
    catch(_){
      showErrorMessage("Erreur lors du chargement de la caméra");
    }
  }

  /// @brief Lance l'enregistrement de la section actuelle
  @protected
  void startRecord() async {
    if(controller == null){
      return;
    }

    startedRecordingCurrentSection = true;

    // lancement de l'enregistrement vidéo
    await controller!.startVideoRecording();

    // lancement du timer
    if(timer != null){
      timer!.cancel();
    }

    timer = Timer.periodic(
      const Duration(seconds: 1),
      (time) {
        setState(() {
          timerSeconds--;

          if (timerSeconds <= 0) {
            timer!.cancel();
            endRecord();
          }
        });
      }
    );
  }

  @protected
  /// @brief Met fin à l'enregistrement
  void endRecord() async{
    if(controller == null){
      return;
    }

    // récupération de la vidéo
    var video = await controller!.stopVideoRecording();

    // stockage dans la liste des sections traitées
    var treatedSection = Map.from(toDo.removeAt(0));

    // ajout de la vidéo et de la preview

    var thumbnail = await VideoThumbnail.thumbnailData(video: video.path,quality: 100);

    treatedSection["preview"] = thumbnail != null ? Image.memory(thumbnail,fit: BoxFit.cover,) : null;
    treatedSection["video"] = video;

    // réinitialisation des valeurs
    if(timer != null){
      timer!.cancel();
    }

    setState((){
      alreadyDone.add(treatedSection.cast());
      videoPaths.add(video.path);

      startedRecordingCurrentSection = false;

      if(toDo.isNotEmpty){
        timerSeconds = toDo[0].cast()["duration"];
      }
    });
  }

  /// @brief Fonction pour envoyer des vidéos à un serveur
  Future<void> sendVideos(String url, List<String> videoPaths) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse(url));
      var key = 'c27f9aad7c97689dffe026a2482bb3878dffbe78ae0e79e90638c72fcc545227';
      // Génération de la signature basée sur les chemins des vidéos et la clé
      var signature = await generateSignature(videoPaths, key);

      // Ajout des fichiers vidéo à la requête
      request.files.add(await http.MultipartFile.fromPath(
        'front_video',
        videoPaths[0],
      ));

      request.files.add(await http.MultipartFile.fromPath(
        'front_head_move_video',
        videoPaths[1],
      ));

      request.files.add(await http.MultipartFile.fromPath(
        'profile_head_up_video',
        videoPaths[2],
      ));

      request.files.add(await http.MultipartFile.fromPath(
        'profile_head_down_video',
        videoPaths[3],
      ));

      request.headers.addAll({
        'Content-Type': 'multipart/form-data',
        'Signature': signature,
      });

      // Envoi de la requête au serveur
      var response = await request.send();
      print(response.statusCode);
      // Lecture de la réponse du serveur
      var responseBody = await response.stream.bytesToString();
      print(responseBody);

      if (response.statusCode == 200) {
        print('Videos have been sent');
      } else {
        print('Error: ${response.statusCode}');
      }
    } catch (e) {
      print('Server error: $e');
    }
  }

  /// @brief Fonction pour générer une signature HMAC SHA-256
  Future<String> generateSignature(List<String> videoPaths, String key) async {
    var keyBytes = utf8.encode(key);
    var hmac = Hmac(sha256, keyBytes);

    // Accumulation des données des fichiers vidéo
    var accumulatedData = BytesBuilder();

    // Lecture des bytes de chaque fichier vidéo
    for (var path in videoPaths) {
      var fileBytes = await File(path).readAsBytes();
      accumulatedData.add(fileBytes);
    }

    // Génération de la signature
    var message = accumulatedData.toBytes();
    var digest = hmac.convert(message);

    return digest.toString();
  }

  @protected
  /// @brief Affiche un message d'erreur sous forme d'alerte
  /// @param errorMessage le message d'erreur
  void showErrorMessage(String errorMessage){
    print(errorMessage);
  }
}


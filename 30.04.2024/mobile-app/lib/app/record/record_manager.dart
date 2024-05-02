import 'dart:async';

import 'package:camera/camera.dart';

/// @brief Configuration d'enregistrement
class RecordManager{
  /// @brief Gestionnaire de la caméra
  CameraController? camera;

  /// @brief Si l'enregistrement est en cours
  bool isRecording = false;

  /// @brief Si l'enregistrement est en pause
  bool isInPause = false;

  /// @brief Preview de la caméra
  late CameraPreview preview;

  /// @brief Durée de vidéo enregistrée
  int registeredDuration = 0;

  /// @brief Gestionnaire de durée
  late Timer timer;

  /// @brief Action à faire à l'incrémentation du timer
  void Function()? toDoOnTimerIncrement;

  /// @brief Dernière vidéo enregistrée
  XFile? lastRecordedVideo;

  /// @brief Met à jour le controller et crée la preview
  /// @param controller le controller
  void setController({required CameraController controller}){
    camera = controller;
    preview = CameraPreview(camera!);
  }

  /// @brief Lance l'enregistrement et le compteur de temps
  /// @param toDoOnTimerIncrement action à appeler à l'incrémentation du timer
  /// @param imageManager action à appeler à la réception d'une frame
  void startRecord({void Function()? toDoOnTimerIncrement,void Function(CameraImage)? imageManager}){
    this.toDoOnTimerIncrement = toDoOnTimerIncrement;
    lastRecordedVideo = null;
    isRecording = true;

    camera!.startVideoRecording(onAvailable: (CameraImage frame){
      if(imageManager != null && isRecording){
        imageManager(frame);
      }
    });

    // lancement du timer
    launchTimer();
  }

  /// @brief Stoppe l'enregistrement
  void pauseRecord(){
    camera!.pauseVideoRecording();
    isInPause = true;
    timer.cancel();
  }

  /// @brief Stoppe la pause et redémarre
  void resumeRecord(){
    camera!.resumeVideoRecording();
    isInPause = false;
    launchTimer();
  }

  /// @brief Stoppe l'enregistrement
  Future<void> stopRecord() async{
    timer.cancel();
    isRecording = false;
    isInPause = false;
    registeredDuration = 0;
    toDoOnTimerIncrement = null;
    lastRecordedVideo = await camera!.stopVideoRecording();
  }

  /// @brief Lance le timer
  void launchTimer(){
    timer = Timer.periodic(const Duration(seconds: 1),(time) {
      registeredDuration++;

      if(toDoOnTimerIncrement != null){
        toDoOnTimerIncrement!();
      }
    }
    );
  }

  /// @return La dernière vidéo enregistrée
  XFile? getLastRecordedVideo(){
    return lastRecordedVideo;
  }
}


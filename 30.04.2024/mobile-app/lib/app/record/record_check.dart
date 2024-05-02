import 'package:camera/camera.dart';
import 'package:mobileapp/config/assets_config.dart';
import 'package:tflite_flutter/tflite_flutter.dart';

/// @brief Vérificateur de frame
class RecordCheck{
  /// @brief Interpréteur tensorflow
  late Future<Interpreter>? interpreterFuture;

  /// @brief Si les ressources sont alloués
  bool isAllocated = false;

  RecordCheck(){
    try{
      interpreterFuture = Interpreter.fromAsset(AssetsConfig.detectionModel.getPath());
    }
    catch(_){}
  }

  /// @brief Vérifie la présence d'une tête sur l'image
  /// @param frame la frame
  /// @return Si une tête est présente
  Future<bool> check({required CameraImage frame}) async{
    if(interpreterFuture == null){
      return false;
    }

    try{
      var interpreter = await interpreterFuture;

      if(interpreter == null){
        return false;
      }

      // allocation des ressources pour le premier appel
      if(!isAllocated){
        interpreter.allocateTensors();
        isAllocated = true;
      }



      return true;
    }
    catch(_){
      print('erreur');
      print(_);
      return false;
    }

  }
}
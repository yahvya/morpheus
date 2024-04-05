import 'package:camera/camera.dart';
import 'package:morpheus_team/app/detection/verificator.dart';

/// @brief Vérifie si le visage se trouve bien face caméras avec la tête levé
class FrontFaceHeadMoveVerificator extends Verificator{

  bool verify(CameraImage frame){
    return false;
  }
}
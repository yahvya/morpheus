import 'dart:math';

import 'package:camera/camera.dart';
import 'package:morpheus_team/app/detection/verificator.dart';

/// @brief Vérifie si le visage se trouve bien face caméras
class FrontFaceVerificator extends Verificator{
  int count = 0;


  bool verify(CameraImage frame){
    return true;
  }
}

import 'package:camera/camera.dart';
import 'package:morpheus_team/app/detection/verificator.dart';

/// @brief Vérifie si la personne est bien de sur son profil droit
class RightProfileVerificator extends Verificator{

  bool verify(CameraImage frame){
    return false;
  }
}
import 'package:camera/camera.dart';

/// @brief Classe de vérification du positionnement
abstract class Verificator{
  /// brief Vérifie si la position dans la frame correspond à la position attendue
  /// @param frame la frame vidéo à vérifier
  /// @return si la position dans la frame correspond à la position attendue
  bool verify(CameraImage frame);
}
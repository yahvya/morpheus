import 'package:camera/camera.dart';
import 'package:mobileapp/app/api/Result.dart';

/// @brief contact de l'api
class Contact{
  /// @brief Envoi la vidéo à l'api
  /// @param video la vidéo
  /// @param controller de caméra utilisé
  /// @return Le résultat de l'appel
  Future<Result> contact({required XFile video,required CameraController usedCamera}) async{
    return const Result(successfulyCalled: false,errorMessage: "Une erreur s'est produite");
  }
}
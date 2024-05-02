import 'package:camera/camera.dart';
import 'package:mobileapp/app/api/api_result.dart';
import 'package:mobileapp/app/profiles/profile.dart';

/// @brief contact de l'api
class Contact{
  /// @brief Envoi la vidéo à l'api
  /// @param senderProfile profile de l'utilisateur
  /// @param video la vidéo
  /// @param mallampatiScore score de mallampati choisi
  /// @param usedCamera de caméra utilisé
  /// @return Le résultat de l'appel
  static Future<ApiResult> contact({required Profile senderProfile,required XFile video,required mallampatiScore,required CameraController usedCamera}) async{
    try{
      // appel de l'api
      return Contact.buildResultFrom();
    }
    catch(_){
      return const ApiResult(successfulyCalled: false,errorMessage: "Une erreur s'est produite lors du traitement.");
    }
  }

  /// @brief Formatte la réponse de l'api
  /// @return L'objet résult résultant
  static ApiResult buildResultFrom(){
    return const ApiResult(
      successfulyCalled: true,
      textualsDatas: {
        "Ouverture maximum de la bouche" : "8cm",
        "Distance maximum du levé de tête": "10cm" 
      }
    );
  }
}
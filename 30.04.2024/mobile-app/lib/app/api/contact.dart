import 'dart:convert';

import 'package:camera/camera.dart';
import 'package:mobileapp/app/api/api_result.dart';
import 'package:mobileapp/app/profiles/profile.dart';
import 'package:http/http.dart' as http;
import 'package:mobileapp/app/utils/json_assets_reader.dart';
import 'package:mobileapp/config/assets_config.dart';
import 'package:encrypt/encrypt.dart';

/// @brief contact de l'api
class Contact{
  /// @brief Envoi la vidéo à l'api
  /// @param senderProfile profile de l'utilisateur
  /// @param video la vidéo
  /// @param mallampatiScore score de mallampati choisi
  /// @param mobilityGradeScore score de mobilité de bouche
  /// @param usedCamera de caméra utilisé
  /// @return Le résultat de l'appel
  static Future<ApiResult> contact({required Profile senderProfile,required XFile video,required int mallampatiScore,required int mobilityGradeScore,required CameraController usedCamera}) async{
    try{
      // récupération de la configuration de l'api
      var readResult = await JsonAssetsReader.get(toRead: AssetsConfig.apiConfig);

      if(readResult == null){
        return const ApiResult(
          successfulyCalled: false,
          errorMessage: "Echec de récupération de la configuration"
        );
      }

      readResult = readResult as Map<String,dynamic>;

      String? signature = buildSignature(
        expectedMessage: readResult["expected-message"] as String,
        encryptKey: readResult["key"] as String
      );  

      if(signature == null){
        return const ApiResult(successfulyCalled: false,errorMessage: "Une erreur s'est produite");
      }

      // création de la requête
      http.MultipartRequest request = http.MultipartRequest(
        "POST",
        Uri.parse(readResult["link"] as String)
      );

      // création des en-têtes
      request.headers["signature"] = signature;
      request.fields["mallampati_score"] = mallampatiScore.toString();
      request.fields["mobility_grade_score"] = mobilityGradeScore.toString();
      request.fields["username"] = senderProfile.fullname;
      request.fields["user_email"] = senderProfile.email;
      request.files.add(
        await http.MultipartFile.fromPath("video",video.path)
      );

      return await Contact.buildResultFrom(response: await request.send());
    }
    catch(_){
      return const ApiResult(successfulyCalled: false,errorMessage: "Une erreur s'est produite lors du traitement.");
    }
  }

  /// @brief Construis la signature de vérification
  /// @return Signature de vérification de requête
  static String? buildSignature({required String expectedMessage,required String encryptKey}){
    try{
      Encrypter encrypter = Encrypter(
        Fernet(
          Key.fromBase64(encryptKey)
        )
      );

      return encrypter.encrypt(expectedMessage).base64;
    }
    catch(_){
      return null;
    }
  }

  /// @brief Formatte la réponse de l'api
  /// @param response réponse de l'api
  /// @return L'objet résult résultant
  static Future<ApiResult> buildResultFrom({required http.StreamedResponse response}) async{
    String responseStr = await response.stream.bytesToString();

    var parsedResponse = json.decode(responseStr) as Map<String,dynamic>;

    // erreur de l'api
    if(!(parsedResponse["success"] as bool)){
      return ApiResult(
        successfulyCalled: false,
        errorMessage: parsedResponse["error"] as String
      );
    }

    Map<String,dynamic> datas = parsedResponse["datas"] as Map<String,dynamic>;

    // récupération et conversion des données textuelles
    Map<String,String> textualDatas = {};

    (datas["textualDatas"] as Map<String,dynamic>).forEach((key, value) { 
      textualDatas[key] = value as String;
    });

    return ApiResult(
      successfulyCalled: true,
      textualsDatas: textualDatas
    );
  }
}

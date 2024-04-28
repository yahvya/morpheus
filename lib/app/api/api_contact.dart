import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:crypto/crypto.dart';
import 'package:morpheus_team/app/detection/detection_config.dart';

/// @brief Gestionnaire d'échange avec l'api
class ApiContact{
  /// @brief Lien de contact de l'api
  static String defaultLink = "http://192.168.1.114:8000/video";

  /// @brief Fonction pour envoyer des vidéos à l'api serveur
  static Future<bool> sendVideos(String url, Map<int,String> videoPaths) async {
    try {
      if(videoPaths.length < 4) {
        return false;
      }

      var request = http.MultipartRequest('POST', Uri.parse(url));
      var key = 'c27f9aad7c97689dffe026a2482bb3878dffbe78ae0e79e90638c72fcc545227';
      // Génération de la signature basée sur les chemins des vidéos et la clé
      List<String> organizedList = [];

      var keys = videoPaths.keys.toList();

      keys.sort();

      for(var key in keys){
        organizedList.add(videoPaths[key]!);
      }

      var signature = await ApiContact.generateSignature(organizedList, key);

      // Ajout des fichiers vidéo à la requête
      request.files.add(await http.MultipartFile.fromPath(
        'front_video',
        videoPaths[DetectionManager.config[0]["index"]]!,
      ));

      request.files.add(await http.MultipartFile.fromPath(
        'front_head_move_video',
        videoPaths[DetectionManager.config[1]["index"]]!,
      ));

      request.files.add(await http.MultipartFile.fromPath(
        'profile_head_up_video',
        videoPaths[DetectionManager.config[2]["index"]]!,
      ));

      request.files.add(await http.MultipartFile.fromPath(
        'profile_head_down_video',
        videoPaths[DetectionManager.config[3]["index"]]!,
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
        return true;
      } else {
        print('Error: ${response.statusCode}');
      }
    } catch (e) {
      print('Server error: $e');
    }

    return false;
  }

  /// @brief Fonction pour générer une signature HMAC SHA-256
  static Future<String> generateSignature(List<String> videoPaths, String key) async {
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
}

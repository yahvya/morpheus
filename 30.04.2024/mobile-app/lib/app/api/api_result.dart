import 'package:http/http.dart' as http;

/// @brief Résultat d'appel à l'api
class ApiResult{
  const ApiResult({
    required this.successfulyCalled,
    this.errorMessage,
    this.resultVideo,
    this.textualsDatas = const {}
  });

  /// @brief Si l'appel à réussi
  final bool successfulyCalled;

  /// @brief Message d'erreur potentiel
  final String? errorMessage;

  /// @brief Map des données textuelles, indicé par le titre de la donnée et ayant comme valeur la donnée textuelle 
  final Map<String,String> textualsDatas;

  /// @brief Vidéo résultante
  final http.MultipartFile? resultVideo;

  /// @brief Enregistre les résultats au format zip
  Future<bool> downloadAsZip() async{
    return true;
  }
}
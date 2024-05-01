import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:mobileapp/config/assets_config.dart';

/// @brief Utilitaire de lecture assets de type JSON
class JsonAssetsReader{
  /// @brief Fourni le contenu d'un asset sous format json
  /// @param toRead assets à récupérer
  /// @return Le contenu décodé ou null
  static Future<dynamic> get({required AssetsConfig toRead}) async{
    try{
      String jsonContent = await rootBundle.loadString(toRead.getPath());

      return json.decode(jsonContent);
    }
    catch(_){
      return null;
    }
  }
}
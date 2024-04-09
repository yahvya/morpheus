import 'dart:convert';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// @brief Chemins des assets de configuration
enum ConfigAssets{
  loggedAccounts(path: "logged-accounts.json");

  const ConfigAssets({required this.path});

  /// @brief Nom du fichier à partir du dossier
  final String path;

  /// @brief Fourni le asset sous format json
  /// @return le contenu json ou null
  Future<dynamic> asJson() async{
   try{
     var content = await const FlutterSecureStorage().read(key: path);

      return content != null ? jsonDecode(content) : null;
   }
   catch(_){
      return null;
   }
  }

  /// @brief Sauvegarde le nouveau contenu de la configuration
  /// @return si la sauvegarde à réussie
  Future<bool> save(String newContent) async{
    try{
      await const FlutterSecureStorage().write(key: path,value: newContent);

      return true;
    }
    catch(_){
      return false;
    }
  }
}

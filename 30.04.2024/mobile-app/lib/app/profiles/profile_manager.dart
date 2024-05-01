import 'dart:convert';

import 'package:mobileapp/app/profiles/profile.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:mobileapp/config/storage_config.dart';

/// @brief Gestionnaire de profil de l'application
class ProfileManager{
  /// @brief Charge les profiles stockés
  /// @return Les profiles
  static Future<List<Profile>> loadProfiles() async{
    try{
      var profiles = await const FlutterSecureStorage().read(key: StorageConfig.authProfiles.key);

      if(profiles == null){
        return [];
      }

      var profilesConfig = json.decode(profiles);

      if(profilesConfig == null){
        return [];
      }

      // conversion des profiles
      return (profilesConfig as List<dynamic>)
        .map((profileConfig){
          profileConfig = profileConfig as Map<String,dynamic>;

          Map<String,String> config = {};

          // conversion de la map dynamique en map de chaîne
          profileConfig.forEach((key, value) { config[key] = value as String; });

          return config;
        })
        .map((profileConfig) => Profile.fromJson(profileConfig: profileConfig)).toList();
    }
    catch(_){
      return [];
    }
  }

  /// @brief Met à jour la liste des profiles
  /// @return Si la mise à jour réussie
  static Future<bool> updateProfiles({required List<Profile> profiles}) async {
    try{
      const FlutterSecureStorage().write(
          key: StorageConfig.authProfiles.key,
          value: json.encode(profiles.map((profile) => profile.toJson()).toList())
      );

      return true;
    }
    catch(_){
      return false;
    }
  }
}
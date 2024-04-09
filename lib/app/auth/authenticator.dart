import 'dart:convert';

import 'package:flutter_bcrypt/flutter_bcrypt.dart';
import 'package:morpheus_team/assets/config_assets.dart';

/// @brief Gestionnaire d'authentification
class Authenticator{
  /// si l'utilisateur est connecté actuellement
  static bool isLogged = false;

  /// configuration actuelle d'authentification
  static Map<String,dynamic>? authConfig;

  /// @brief Initialise l'authentification
  static Future<void> init() async{
    await Authenticator.loadConfig();

    if(Authenticator.authConfig == null){
      await Authenticator.createDefaultConfig();
      await Authenticator.loadConfig();
    }

    Authenticator.isLogged = Authenticator.authConfig!["stay-auth"] as bool;
  }

  /// @brief Vérifie si l'utilisateur est déjà connecté
  /// @return Si l'utilisateur est connecté
  static bool isUserLogged(){
    return Authenticator.isLogged;
  }

  /// @brief Authentifie l'utilisateur ou crée son compte puis l'authentifie
  static Future<bool> authenticateUser(String email,String password, bool stayAuth) async {
    try {
      var authConfig = Authenticator.authConfig!;
      var accounts = (authConfig["accounts"] as Map<String, dynamic>?)!;

      // création d'un nouveau compte
      if (!accounts.containsKey(email)) {
        accounts[email] = await FlutterBcrypt.hashPw(password: password, salt: await FlutterBcrypt.salt());
      }

      // vérification du compte
      if(!await FlutterBcrypt.verify(password: password, hash: accounts[email]!)){
        return false;
      }

      // sauvegarde du nouvel état de configuration
      authConfig["accounts"] = accounts;
      authConfig["stay-auth"] = stayAuth;

      if(! await ConfigAssets.loggedAccounts.save(jsonEncode(authConfig))){
        return false;
      }

      Authenticator.authConfig = authConfig;
      Authenticator.isLogged = true;

      return true;
    }
    catch(_){
      return false;
    }
  }

  /// @brief Charge la configuration
  static loadConfig() async{
    Authenticator.authConfig = await ConfigAssets.loggedAccounts.asJson() as Map<String,dynamic>?;
  }

  /// @brief Crée la configuration par défaut
  static createDefaultConfig() async{
    await ConfigAssets.loggedAccounts.save(jsonEncode({
      "stay-auth": false,
      "accounts": {}
    }));
  }
}

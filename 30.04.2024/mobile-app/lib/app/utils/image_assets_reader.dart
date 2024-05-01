import 'package:flutter/cupertino.dart';
import 'package:mobileapp/config/assets_config.dart';

/// @brief Lecteur de ressource d'image
class ImageAssetsReader{
  /// @brief Fourni la ressource image
  /// @para imageConfig Configuration de l'image
  /// @return l'image au format AssetImage
  static AssetImage? getImageFrom(AssetsConfig imageConfig){
    try{
      return AssetImage(imageConfig.getPath());
    }
    catch(_){
      return null;
    }
  }
}
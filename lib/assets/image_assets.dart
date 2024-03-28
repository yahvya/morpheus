import 'package:flutter/cupertino.dart';

/// @brief Chemins des assets images
enum ImageAssets{
  favicon(path: "favicon.png"),
  tap(path: "tap.png"),
  rec(path: "rec.png");

  const ImageAssets({required this.path});

  /// @brief Nom du fichier à partir du dossier
  final String path;

  /// @param width largeur de l'image
  /// @param height hauteur de l'image
  /// @return L'image
  Image image({int width = 70,int height = 70}){
    return Image(
        image: ResizeImage(AssetImage("assets/images/$path"),
          width: width,
          height: height,
          allowUpscaling: true
        )
    );
  }
}

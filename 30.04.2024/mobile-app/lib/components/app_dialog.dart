import 'package:flutter/material.dart';
import 'package:mobileapp/app/utils/image_assets_reader.dart';
import 'package:mobileapp/config/assets_config.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/theme/app_theme.dart';

/// @brief Boîte de dialogue customisé
class AppDialog extends StatelessWidget{
  const AppDialog({super.key,required this.message,required this.buttonsRow});

  /// @brief Message du dialogue
  final String message;

  /// @brief Zone des boutons
  final Widget buttonsRow;

  @override
  build(BuildContext context){
    return Dialog(
      child: FractionallySizedBox(
        heightFactor: 0.4,
        child: Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
              color: AppTheme.upperBackgroundColor.color,
              borderRadius:  BorderRadius.circular(10)
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Image(image: ResizeImage(
                ImageAssetsReader.getImageFrom(AssetsConfig.logoImage)!,
                width: 60,
                height: 50
              )),
              PageModel.specialText(
                text: message,
                size: 18,
                color: AppTheme.upperText.color
              ),
              const SizedBox(height: 40),
              buttonsRow
            ],
          ),
        ),
      )
    );
    // return FractionallySizedBox(
    //   heightFactor: 0.4,
    //   widthFactor: 0.8,
    //   child:
    // );
  }
}
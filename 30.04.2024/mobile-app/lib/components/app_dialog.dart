import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
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
              borderRadius: const BorderRadius.all(Radius.circular(10))
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
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
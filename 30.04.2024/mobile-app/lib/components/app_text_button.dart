import 'package:flutter/material.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/theme/app_theme.dart';

/// @brief Bouton d'icône
class AppTextButton extends StatelessWidget{
  const AppTextButton({super.key,required this.text,this.onClick});

  /// @brief Texte du bouton
  final String text;

  /// @brief Action à exécuter au click sur le bouton
  final void Function()? onClick;

  @override
  build(BuildContext context){
    var upperColorState = MaterialStateProperty.all(AppTheme.specialText.color);

    return TextButton(
      onPressed: onClick,
      child: PageModel.basicText(
        text: text,
        color: AppTheme.specialText.color
      ),
      style: ButtonStyle(
        padding: MaterialStateProperty.all(const EdgeInsets.all(5)),
        shape: MaterialStateProperty.all(RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(3)
        )),
        backgroundColor: MaterialStateProperty.all(AppTheme.specialBackgroundColor.color),
        foregroundColor: upperColorState,
      ),
    );
  }
}
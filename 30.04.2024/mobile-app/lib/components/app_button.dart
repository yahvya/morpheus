import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/theme/app_theme.dart';

class AppButton extends StatelessWidget{
  const AppButton({super.key,required this.text,required this.icon,this.onPressed,this.size});

  /// @brief Texte du bouton
  final String text;

  /// @brief Icône associé au bouton
  final IconData icon;

  /// @brief Action à faire au click
  final void Function()? onPressed;

  /// @brief Taille du bouton
  final MaterialStateProperty<Size>? size;

  @override
  build(BuildContext context){
    var upperColorState = MaterialStateProperty.all(AppTheme.specialText.color);

    return ElevatedButton.icon(
      onPressed: onPressed,
      icon: Icon(icon),
      label: PageModel.basicText(text: text,color: AppTheme.specialText.color),
      style: ButtonStyle(
        padding: MaterialStateProperty.all(const EdgeInsets.all(15)),
        shape: MaterialStateProperty.all(RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10)
        )),
        textStyle: MaterialStateProperty.all(TextStyle(
          color: AppTheme.specialText.color,
          fontFamily: "Poppins",
          fontSize: 18
        )),
        backgroundColor: MaterialStateProperty.all(AppTheme.specialBackgroundColor.color),
        foregroundColor: upperColorState,
        minimumSize: size,
      ),
    );
  }
}
import 'package:flutter/cupertino.dart';
import 'package:mobileapp/pages/page_model.dart';

import '../theme/app_theme.dart';

/// @brief Affichage de message statique
class AppMessage extends StatelessWidget{
  const AppMessage({super.key, required this.message});

  final String message;

  @override
  build(BuildContext context){
    return Container(
      decoration: BoxDecoration(
        color: AppTheme.upperBackgroundColor.color,
        borderRadius:  BorderRadius.circular(5)
      ),
      padding: const EdgeInsets.all(20),
      child: PageModel.basicText(text: message,size: 15),
    );
  }
}
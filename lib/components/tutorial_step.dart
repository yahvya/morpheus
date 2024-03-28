import 'package:flutter/cupertino.dart';
import 'package:morpheus_team/style-config/app_theme.dart';

/// @brief étape de tutoriel
class TutorialStep extends StatelessWidget{
  const TutorialStep({super.key,required this.description,required this.stepCount,required this.image});

  /// @brief description du tutoriel
  final String description;

  /// @brief numéro d'étape du tutoriel
  final int stepCount;

  /// @brief Image de tutoriel
  final Image image;

  @override
  Widget build(BuildContext context){
    return FractionallySizedBox(
      widthFactor: 0.85,
      child: Center(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            image,
            const SizedBox(width: 40,),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    margin: const EdgeInsets.only(left: 20),
                    child: Text(
                      "$stepCount.",
                      style: const TextStyle(
                          color: AppTheme.special,
                          fontSize: 60,
                          fontWeight: FontWeight.bold
                      ),
                    ),
                  ),
                  Text(
                    description,
                    style: const TextStyle(
                      color: AppTheme.textOnBackground,
                      fontSize: 25,
                    ),
                    softWrap: true,
                  )
                ],
              ),
            ),
            const SizedBox(height: 100,)
          ],
        ),
      ),
    );
  }
}

import 'package:flutter/cupertino.dart';
import 'package:mobileapp/app/profiles/profile.dart';
import 'package:mobileapp/pages/page_model.dart';

/// @brief Page d'enregistrement
class RecordPage extends StatelessWidget{
  const RecordPage({super.key,required this.usedProfile});

  /// @brief Profil de l'utilisateur entrain d'enregistrer
  final Profile usedProfile;

  @override
  build(BuildContext context){
    return PageModel.buildPage(Column(
      children: [],
    ));
  }
}
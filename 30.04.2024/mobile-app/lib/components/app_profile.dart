import 'package:flutter/material.dart';
import 'package:mobileapp/app/profiles/profile.dart';
import 'package:mobileapp/components/app_icon_button.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/theme/app_theme.dart';
import 'package:mobileapp/app/utils/string_extensions.dart';

/// @brief Composant de gestion d'un profil
class AppProfile extends StatelessWidget{
  const AppProfile({required this.profile,this.index,this.onClick,this.onDelete});

  /// @brief Profil
  final Profile profile;

  /// @brief Index utilitaire potentiel
  final int? index;

  /// @brief Action à exécuter au click sur le profil
  final void Function(int?)? onClick;

  /// @brief Action à exécuté au click sur la suppression (prend en paramètre l'index fourni)
  final void Function(int?)? onDelete;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: AppTheme.upperBackgroundColor.color,
        borderRadius: const BorderRadius.all(Radius.circular(5) )
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          buildInfZone(),
          buildDeleteButton()
        ],
      ),
    );
  }

  /// @brief Construis la zone des informations du profil
  /// @return l'affichage crée
  Widget buildInfZone(){
    return GestureDetector(
      onTap: (){
        if(onClick != null){
          onClick!(index);
        }
      },
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          PageModel.specialText(
            text: profile.fullname.capitalize(),
            size: 17,
            color: AppTheme.upperText.color
          ),
           const SizedBox(height: 10,),
          PageModel.basicText(
            text: profile.email,
            size: 13,
            color: AppTheme.upperText.color
          )
        ],
      ),
    );
  }

  /// @brief Construis le bouton de suppression
  /// @return le bouton
  Widget buildDeleteButton(){
    return AppIconButton(
      icon: Icons.delete,
      onClick: (){
        if(onDelete != null){
          onDelete!(index);
        }
      }
    );
  }
}
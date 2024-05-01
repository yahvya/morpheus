import 'package:flutter/cupertino.dart';
import 'package:mobileapp/app/profiles/profile.dart';

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
    return Row(
      children: [
        Text(profile.fullname)
      ],
    );
  }

}
import 'package:flutter/material.dart';
import 'package:mobileapp/app/profiles/profile_manager.dart';
import 'package:mobileapp/components/app_button.dart';
import 'package:mobileapp/components/app_dialog.dart';
import 'package:mobileapp/components/app_text_button.dart';
import 'package:mobileapp/pages/page_model.dart';

import '../app/profiles/profile.dart';
import '../components/app_message.dart';
import '../components/app_profile.dart';

/// @brief Page de gestion / choix des profils
class ProfilePage extends StatefulWidget{
  const ProfilePage({required this.profiles});

  /// @brief Liste des profiles
  final List<Profile> profiles;

  @override
  State<StatefulWidget> createState() {
    return ProfilePageState(profiles: profiles);
  }
}

class ProfilePageState extends State<ProfilePage>{
  ProfilePageState({required this.profiles});

  /// @brief Liste des profiles
  final List<Profile> profiles;

  @override
  build(BuildContext context){
    return PageModel.buildPage(SafeArea(
      child: Center(
        child: Container(
          padding: const EdgeInsets.only(bottom: 50),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                children: [
                  const SizedBox(height: 30,),
                  PageModel.specialText(text: "Choix du profil".toUpperCase()),
                  const SizedBox(height: 60),
                  getListZone()
                ],
              ),
              AppButton(
                text: "Nouveau profil",
                icon: Icons.add_circle,
                size: MaterialStateProperty.all(Size(MediaQuery.of(context).size.width - 70,60)),
              )
            ],
          ),
        ),
      ),
    ));
  }

  /// @brief Construis l'affichage de la liste des produits
  /// @param context le contexte
  /// @return L'affichage construis
  List<Widget> buildProfilesView({required BuildContext context}){
    SizedBox separator = const SizedBox(height: 30);
    return [
      const SizedBox(height: 30),
      FractionallySizedBox(
        widthFactor: 0.90,
        child: Column(
          children: [
            const AppMessage(message: "Cliquez sur un profil pour démarrer l'enregistrement"),
            const SizedBox(height: 40),
            SizedBox(
              height: MediaQuery.of(context).size.height / 2,
              child: ListView.separated(
                  itemBuilder: (BuildContext context,int index){
                    return AppProfile(
                      profile: profiles[index],
                      index: index,
                      onClick: (int? index) => showRecordPage(index: index!),
                      onDelete: (int? index) => deleteProfile(index: index!,context: context),
                    );
                  },
                  separatorBuilder: (BuildContext context,int index) => separator,
                  itemCount: profiles.length
              ),
            )
          ],
        )
      )
    ];
  }

  /// @return La zone d'affichage de list
  Widget getListZone(){
    return profiles.isEmpty ?
      const FractionallySizedBox(
        widthFactor: 0.90,
        child: AppMessage(message: "Aucun profil trouvé, veuillez créer un profil"),
      ) :
      Column(children: buildProfilesView(context: context),);
  }

  /// @brief Affiche la page d'enregistrement
  /// @param index index du profil
  void showRecordPage({required int index}){

  }

  /// @brief Supprime un profil et met à jour l'écran
  /// @param index index du profil
  void deleteProfile({required int index,required BuildContext context}){
    showDialog(
      barrierDismissible: false,
      context: context,
      builder: (BuildContext builderContext) => AppDialog(
        message: "Êtes-vous sûr de vouloir supprimer ce profil ?",
        buttonsRow: buildValidationButtons(index: index,builderContext: builderContext)
      )
    );
  }

  /// @brief Construis les boutons de validation
  /// @param index Index du profil
  /// @param builderContext contexte de construction du dialogue
  /// @return les boutons construits
  Widget buildValidationButtons({required int index,required BuildContext builderContext}){
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        AppTextButton(
          text: "Annuler",
          onClick: () => Navigator.pop(builderContext),
        ),
        const SizedBox(width: 30,),
        AppTextButton(
          text: "Oui",
          onClick: (){
            Navigator.pop(builderContext);
            validateDeleteOf(index: index);
          },
        ),
      ],
    );
  }

  /// @brief Valide la suppression d'un profil
  /// @param index index du profil à supprimer
  void validateDeleteOf({required int index}){
    try{
      var deletedProfile = profiles.removeAt(index);

      ProfileManager.updateProfiles(profiles: profiles).then((success){
        if(!success) {
          profiles.insert(index,deletedProfile);
          return;
        }

        setState((){});
      });
    }
    catch(_){}
  }
}
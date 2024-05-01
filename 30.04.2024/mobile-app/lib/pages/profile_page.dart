import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobileapp/app/profiles/profile_manager.dart';
import 'package:mobileapp/components/app_button.dart';
import 'package:mobileapp/components/app_dialog.dart';
import 'package:mobileapp/components/app_profile_creator.dart';
import 'package:mobileapp/components/app_text_button.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/pages/record_page.dart';

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
              buildNewProfileButton(context: context)
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
                      onClick: (int? index) => showRecordPage(index: index!,context: context),
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
  /// @param context contexte de création
  void showRecordPage({required int index,required BuildContext context}){
    Navigator.of(context).push(MaterialPageRoute(builder: (BuildContext context) => RecordPage(usedProfile: profiles[index])));
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

  /// @brief Construis le bouton et gère la création de nouveau profil
  /// @param context contexte de création
  /// @return le bouton
  AppButton buildNewProfileButton({required BuildContext context}){
    return AppButton(
      text: "Nouveau profil",
      icon: Icons.add_circle,
      size: MaterialStateProperty.all(Size(MediaQuery.of(context).size.width - 70,60)),
      onPressed: (){
        showDialog(
          barrierDismissible: false,
          context: context,
          builder: (BuildContext builderContext){
            return AppProfileCreator(
              builderContext: builderContext,
              onCreate: (Profile createdProfile) => tryCreateProfile(profile: createdProfile)
            );
          }
        );
      },
    );
  }

  /// @brief Tente de créer le profil
  /// @param profile le profile à créer
  /// @return null si la création réussi ou message d'erreur
  Future<String?> tryCreateProfile({required Profile profile}) async{
    try{
      if(profile.fullname.isEmpty){
        return "Le nom ne peut pas être vide";
      }

      if(profile.email.isEmpty){
        return "L'email ne peut pas être vide";
      }

      // vérification d'existence du profil
      for(Profile p in profiles){
        if(p.email == profile.email){
          return "Cet email est déjà associé au profil de '${p.fullname}'";
        }
      }

      profiles.add(profile);

      bool success = await ProfileManager.updateProfiles(profiles: profiles);

      if(!success){
        profiles.remove(profile);
        return "Une erreur s'est produite lors de création du profil";
      }

      setState(() {});

      return null;
    }
    catch(_){
      return "Une erreur s'est produite lors de création du profil";
    }
  }
}
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:mobileapp/app/profiles/profile_manager.dart';
import 'package:mobileapp/components/app_button.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/theme/app_theme.dart';

import '../app/profiles/profile.dart';
import '../components/app_profile.dart';

/// @brief Page de gestion des profils
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
    return PageModel.buildPage(Center(
      child: Container(
        padding: const EdgeInsets.only(bottom: 30),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              children: [
                const SizedBox(height: 70,),
                PageModel.specialText(text: "Gestion des profils".toUpperCase()),
                const SizedBox(height: 60),
                Container(
                  padding: const EdgeInsets.only(bottom: 30),
                  height: 350,
                  child: FractionallySizedBox(
                    heightFactor: 1,
                    widthFactor: 0.8,
                    child: Container(
                      decoration: BoxDecoration(
                          border: Border(
                              bottom: BorderSide(
                                  color: AppTheme.specialBackgroundColor.color
                              )
                          )
                      ),
                      height: 350,
                      child: profiles.isEmpty ? PageModel.basicText(text: "Aucun profil trouvé, veuillez créer un profil") : buildProfilesView(),
                    )
                  ),
                )
              ],
            ),
            AppButton(
              text: "Nouveau profil",
              icon: Icons.add,
              size: MaterialStateProperty.all(const Size(300,20)),
            )
          ],
        ),
      ),
    ));
  }

  ListView buildProfilesView(){
    SizedBox separator = const SizedBox(height: 30);

    return ListView.separated(
        itemBuilder: (BuildContext context,int index){
          return AppProfile(
            profile: profiles[index],
            index: index,
            onClick: (int? index) => showRecordPage(profileIndex: index!),
            onDelete: (int? index) => deleteProfile(index: index!),
          );
        },
        separatorBuilder: (BuildContext context,int index) => separator,
        itemCount: profiles.length
    );
  }

  /// @brief Affiche la page d'enregistrement
  void showRecordPage({required int profileIndex}){

  }

  void deleteProfile({required int index}){
    try{
      ProfileManager.updateProfiles(profiles: profiles).then((success){
        if(!success) {
          return;
        }

        setState((){
          profiles.removeAt(index);
        });
      });
    }
    catch(_){}
  }
}
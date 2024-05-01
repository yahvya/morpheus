import 'package:flutter/material.dart';
import 'package:mobileapp/app/profiles/profile.dart';
import 'package:mobileapp/components/app_input.dart';
import 'package:mobileapp/components/app_text_button.dart';
import 'package:mobileapp/pages/page_model.dart';
import 'package:mobileapp/theme/app_theme.dart';
import 'package:mobileapp/app/utils/image_assets_reader.dart';
import 'package:mobileapp/config/assets_config.dart';

/// @brief Dialogue de création de profil
class AppProfileCreator extends StatefulWidget{
  const AppProfileCreator({super.key,required this.builderContext,required this.onCreate,this.onCancel});

  /// @brief Contexte d'affichage du dialogue
  final BuildContext builderContext;

  /// @brief Action à exécuter une fois le profil crée (prend en paramètre le nouveau profil) renvoi null en cas de validation ou un message d'erreur
  final Future<String?> Function(Profile) onCreate;

  /// @brief Action à exécuter en cas d'annulation
  final Future<void> Function()? onCancel;

  @override
  State<StatefulWidget> createState() {
    return AppProfileCreatorState();
  }
}

/// @brief Etat du dialogue
class AppProfileCreatorState extends State<AppProfileCreator>{
  /// @brief Nom complet de la personne
  late String fullname;

  /// @brief Email de la personne
  late String email;

  /// @brief Message d'erreur
  String errorMessage = "";

  @override
  Widget build(BuildContext context){
    return Dialog(
      child: SingleChildScrollView(
        child: Container(
          padding: const EdgeInsets.all(15),
          decoration: BoxDecoration(
              color: AppTheme.upperBackgroundColor.color,
              borderRadius: BorderRadius.circular(10)
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Image(image: ResizeImage(
                ImageAssetsReader.getImageFrom(AssetsConfig.logoImage)!,
                width: 60,
                height: 50
              )),
              Column(
                children: [
                  const SizedBox(height: 30,),
                  PageModel.specialText(
                    text: "Créez un nouveau profil",
                    color: AppTheme.specialText.color,
                    size: 23
                  ),
                  const SizedBox(height: 20),
                  PageModel.basicText(
                    text: errorMessage,
                    color: AppTheme.specialText.color,
                    size: 15
                  ),
                  const SizedBox(height: 20),
                ],
              ),
              buildForm(context: context),
              const SizedBox(height: 40),
              buildValidationButtons(context: context)
            ],
          ),
        ),
      )
    );
  }

  /// @brief Construis le formulaire de saisie des données
  /// @param context contexte de création
  /// @return Le formulaire
  Column buildForm({required BuildContext context}){
    return Column(
      children: [
        AppInput(
          placeholder: "Nom complet",
          onChanged: (String newFullname){
            fullname = newFullname;
          },
        ),
        const SizedBox(height: 25),
        AppInput(
          placeholder: "Email",
          onChanged: (String newEmail){
            email = newEmail;
          },
        ),
      ],
    );
  }

  /// @brief Construis les boutons de validation
  /// @param context contexte de création
  /// @return les boutons
  Row buildValidationButtons({required BuildContext context}){
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        AppTextButton(
          text: "Annuler",
          onClick: () => manageCancel(context: context),
        ),
        const SizedBox(width: 30,),
        AppTextButton(
          text: "Créer",
          onClick: () => manageCreation(context: context),
        ),
      ]
    );
  }

  /// @brief Gère l'annulation de la création et ferme la popup
  /// @param context contexte de création
  void manageCancel({required BuildContext context}){
    if(widget.onCancel != null){
      widget.onCancel!().then((_) => Navigator.pop(context));
      return;
    }

    Navigator.pop(context);
  }

  /// @brief Gère la création du profil
  /// @param context contexte de création
  void manageCreation({required BuildContext context}){
    Profile createdProfile = Profile(email: email, fullname: fullname);

    widget.onCreate(createdProfile).then((result){
      if(result == null){
        Navigator.pop(context);
        return;
      }

      setState(() {
        errorMessage = result;
      });
    });
  }
}
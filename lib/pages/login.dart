import 'package:flutter/material.dart';
import 'package:morpheus_team/app/auth/authenticator.dart';
import 'package:morpheus_team/assets/image_assets.dart';
import 'package:morpheus_team/components/app_button.dart';
import 'package:morpheus_team/components/app_input.dart';
import 'package:morpheus_team/components/app_checkbox.dart';
import 'package:morpheus_team/pages/home.dart';
import 'package:morpheus_team/style-config/app_theme.dart';

/// @brief Page de connexion
class Login extends StatelessWidget{
  const Login({super.key});

  @override
  Widget build(BuildContext context){
    const baseSpacer = SizedBox(height: 35,);

    String emailValue = "",passwordValue = "";

    bool haveToKeepAuth = true;

    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // favicon
          ImageAssets.favicon.image(width: 100,height: 85),
          baseSpacer,
          // nom de l'application
          const Text(
            "Morpheus",
            style: TextStyle(
              color: AppTheme.special,
              fontSize: 35
            ),
          ),
          const SizedBox(height: 60,),
          // barre d'email
          AppInput(
            placeholder: "Entrez votre email",
            onChanged: (String newValue){ emailValue = newValue; }
          ),
          baseSpacer,
          // barre du mot de passe
          AppInput(
            placeholder: "Entrez votre mot de passe",
            isProtected: true,
            onChanged: (String newValue){ passwordValue = newValue; },
          ),
          const SizedBox(height: 20,),
          // choix de conservation d'état de connexion
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                "Rester connecté",
                style: TextStyle(
                  color: AppTheme.lightTextOnBackground,
                  decoration: TextDecoration.underline,
                  decorationColor: AppTheme.lightTextOnBackground,
                  fontSize: 17
                )
              ),
              const SizedBox(width: 10,),
              AppCheckbox(
                defaultCheckState: haveToKeepAuth,
                onChanged: (bool? checkState){
                  haveToKeepAuth = !haveToKeepAuth;
                }
              )
            ],
          ),
          const SizedBox(height: 45),
          // lancement de l'application
          AppButton(
            containedText: "Lancer l'application",
            onPressed: (){
              // authentification utilisateur
              Authenticator.authenticateUser(emailValue, passwordValue, haveToKeepAuth).then((success){
                if(success){
                  Navigator.of(context).push(MaterialPageRoute(builder: (context) => const Home()));
                }
              });
            }
          )
        ]
      ),
      backgroundColor: AppTheme.background,
    );
  }
}

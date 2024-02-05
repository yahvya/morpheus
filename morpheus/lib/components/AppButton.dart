
import 'package:flutter/cupertino.dart';

/// boutton de l'application
class AppButton extends StatelessWidget{
  final VoidCallback onPressed;

  const AppButton({Key? key, required this.onPressed}) : super(key: key);

  @override
  Widget build(BuildContext context){
    return Container(
      margin: EdgeInsets.fromLTRB(62, 628, 0, 0),
      width: 236,
      height: 52,
      child: ElevatedButton(
        onPressed: onPressed,
        child: Text(
          "Lancer L'application",
          style: TextStyle(
            fontSize: 18,
            color: Colors.white,
          ),
        ),
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all<Color>(Colors.green),
        ),
      ),  
    ),
  }
}

//######################################################################################################
//################## pour lancer l'application veuillez passer ce bout de code pour lancer la fonction #
// AppButton(                                                                                    #
//   onPressed: () {                                                                                   #
//     // Comportement à exécuter lors du clic sur le bouton                                           #
//     print("L'application  est lancée !");                                                    #
//   },                                                                                                #
// )                                                                                                   #
//######################################################################################################

//#####################################################################################################################################################


class LaunchTutorielButton extends StatelessWidget{
  final VoidCallback onPressed;

  const LaunchTutorielButton({Key? key, required this.onPressed}) : super(key: key);

  @override
  Widget build(BuildContext context){
    return Container(
      margin: EdgeInsets.fromLTRB(29, 447, 0, 0),
      width: 289,
      height: 52,
      child: ElevatedButton(
        onPressed: onPressed,
        child: Text(
          "Lancer le tutoriel (icn Aws)",
          style: TextStyle(
            fontSize: 18,
            color: Colors.white,
          ),
        ),
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all<Color>(Colors.green),
        ),
      ),  
    ),
  }
}

//######################################################################################################
//################## pour lancer le tutoriel veuillez passer ce bout de code pour lancer la fonction   #
// LaunchTutorielButton(                                                                               #
//   onPressed: () {                                                                                   #
//     // Comportement à exécuter lors du clic sur le bouton                                           #
//     print("Le tutoriel  est lancé!");                                                               #
//   },                                                                                                #
// )                                                                                                   #
//######################################################################################################
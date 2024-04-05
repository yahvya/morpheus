import 'package:morpheus_team/app/detection/front_face_head_move_verificator.dart';
import 'package:morpheus_team/app/detection/front_face_verificator.dart';
import 'package:morpheus_team/app/detection/left_profile_verificator.dart';
import 'package:morpheus_team/app/detection/right_profile_verificator.dart';

/// @brief Gestionnaire de détection
class DetectionManager{
  /// @brief Configuration des différentes positions de détection
  static List<Map<String, Object>> config = [
    // posture de face (bouche)
    {
      "text": "Face (1)",
      "instructions" : [
      "Prenez la personne de face",
      "Faîtes lui ouvrir la bouche"
      ],
      "duration": 5,
      "verifier": FrontFaceVerificator(),
      "index": 1
    },
    // posture de face (tête levé)
    {
      "text": "Face (2)",
      "instructions" : [
        "Prenez la personne de face",
        "Faîtes lui lever la tête vers l'arrière"
      ],
      "duration": 5,
      "verifier": FrontFaceHeadMoveVerificator(),
      "index": 2
    },
    // posture de profil (tête baissé)
    {
      "text": "Profil (1)",
      "instructions" : [
        "Prenez la personne sur son profil droit",
        "Faîtes lui baisser la tête"
      ],
      "duration": 5,
      "verifier": RightProfileVerificator(),
      "index": 3
    },
    // posture de profil (gauche baissé)
    {
      "text": "Profil (2)",
      "instructions" : [
        "Prenez la personne sur son profil gauche",
        "Faîtes lui baisser la tête"
      ],
      "duration": 5,
      "verifier": LeftProfileVerificator(),
      "index": 4
    },
  ];

  /// @brief Valeurs possible du score de mallampati
  static const mallampatiRange = [1,4];
}

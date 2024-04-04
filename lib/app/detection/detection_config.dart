/// @brief Gestionnaire de détection
class DetectionManager{
  /// @brief Configuration des différentes positions de détection
  static const List<Map<String, Object?>> config = [
    // posture de face (bouche)
    {
      "text": "Face (1)",
      "instructions" : [
      "Prenez la personne de face",
      "Faîtes lui ouvrir la bouche"
      ],
      "duration": 5,
      "verifier": null,
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
      "verifier": null,
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
      "verifier": null,
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
      "verifier": null,
      "index": 4
    },
  ];

  /// @brief Valeurs possible du score de mallampati
  static const mallampatiRange = [1,4];
}

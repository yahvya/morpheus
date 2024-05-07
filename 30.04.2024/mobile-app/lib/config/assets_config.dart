/// @brief Configuration des chemins de ressources
enum AssetsConfig{
  /// @brief Chemin du fichier contenant la configuration d'api
  apiConfig(path: "/api/config.json"),

  /// @brief Chemin du logo de l'application
  logoImage(path: "/images/logo.png"),

  /// @brief Chemin de la class 1 de mallampati
  mallamptiClass1(path: "/detection/mallampati_class_1.png"),

  /// @brief Chemin de la class 2 de mallampati
  mallamptiClass2(path: "/detection/mallampati_class_2.png"),

  /// @brief Chemin de la class 3 de mallampati
  mallamptiClass3(path: "/detection/mallampati_class_3.png"),

  /// @brief Chemin de la class 4 de mallampati
  mallamptiClass4(path: "/detection/mallampati_class_4.png"),

  /// @brief Chemin de l'image de mobilité normal
  normalMobility(path: "/detection/mobility_normal.png"),

  /// @brief Chemin de l'image de mobilité grade 1
  grade1Mobility(path: "/detection/mobility_grade_1.png"),

  /// @brief Chemin de l'image de mobilité grade 2
  grade2Mobility(path: "/detection/mobility_grade_2.png"),

  /// @brief Chemin de l'image de mobilité grade 3
  grade3Mobility(path: "/detection/mobility_grade_3.png");

  const AssetsConfig({required this.path});

  /// @brief Clé de stockage
  final String path;

  /// @return Le chemin concaténé avec le dossier des ressources
  String getPath(){
    return "assets$path";
  }
}

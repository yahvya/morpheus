/// @brief Configuration des chemins de ressources
enum AssetsConfig{
  /// @brief Chemin du fichier contenant la configuration d'api
  apiConfig(path: "/api/config.json");

  const AssetsConfig({required this.path});

  /// @brief Clé de stockage
  final String path;

  /// @return Le chemin concaténé avec le dossier des ressources
  String getPath(){
    return "assets$path";
  }
}
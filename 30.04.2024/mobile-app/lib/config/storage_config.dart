/// @brief Configuration des clés de stockage
enum StorageConfig{
  /// @brief Clé de stockage des profils enregistrés
  authProfiles(key: "AUTH_PROFILES");

  const StorageConfig({required this.key});

  /// @brief Clé de stockage
  final String key;
}
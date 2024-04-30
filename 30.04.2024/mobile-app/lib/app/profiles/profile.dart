/// @brief Profil utilisateur
class Profile{
  const Profile({required this.email,required this.fullname});

  /// @brief Email utilisateur
  final String email;

  /// @brief Nom et prénom utilisateur
  final String fullname;

  /// @return Le profil sous forme de json
  Map<String,String> toJson(){
    return {
      "email": email,
      "fullname": fullname
    };
  }

  /// @brief Crée un profil à partir d'une configuration exportée
  /// @return Le profile crée
  static Profile fromJson({required Map<String,String> profileConfig}){
    return Profile(
      email: profileConfig["email"]!,
      fullname: profileConfig["fullname"]!
    );
  }
}
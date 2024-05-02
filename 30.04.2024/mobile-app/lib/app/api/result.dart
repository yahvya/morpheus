/// @brief Résultat d'appel à l'api
class Result{
  const Result({required this.successfulyCalled,this.errorMessage});

  /// @brief Si l'appel à réussi
  final bool successfulyCalled;

  /// @brief Message d'erreur potentiel
  final String? errorMessage;
}
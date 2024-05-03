/// @brief Extensions sur les chaines de caractères
extension CustomStringExtension on String{
  /// @brief Capitalize la chaine
  /// @return la chaine transformé
  capitalize(){
    return this.split(" ").map((strPart){
      if(strPart.isEmpty){
        return strPart;
      }
      
      strPart = "${strPart[0].toUpperCase()}${strPart.substring(1)}";

      return strPart;
    }).join(" ");
  }
}
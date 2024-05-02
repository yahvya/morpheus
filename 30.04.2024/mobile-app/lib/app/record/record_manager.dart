/// @brief Configuration d'enregistrement
class RecordManager{
  /// @brief Gestionnaire de la caméra
  CameraController? camera;

  /// @brief Si l'enregistrement est en cours
  bool isRecording = false;

  /// @brief Preview de la caméra
  late CameraPreview preview;

  /// @brief Met à jour le controller et crée la preview
  /// @param controller le controller
  void setController({required CameraController controller}){
    camera = controller;
    preview = CameraPreview(camera!);
  }
}
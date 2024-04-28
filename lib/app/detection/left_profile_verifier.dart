import 'package:camera/camera.dart';
import 'package:morpheus_team/app/detection/verifier.dart';
import 'package:google_mlkit_face_detection/src/face_detector.dart';

/// @brief Vérifie si la personne est bien de sur son profil droit
class LeftProfileVerifier extends Verifier{
  LeftProfileVerifier(){
    detector = new FaceDetector(
        options: new FaceDetectorOptions(
          enableLandmarks: true,
          performanceMode: FaceDetectorMode.accurate
        )
    );
  }

  @override
  Future<bool> verify(CameraDescription camera,CameraImage frame) async{
    try{
      // détection du visage
      var detectionResult = await detector.processImage(createImageFromFrame(camera,frame)!);

      if(detectionResult.length != 1)
        return false;

      // vérification de présence des lèvres
      var foundedFace = detectionResult.first;

      return foundedFace.landmarks[FaceLandmarkType.rightEar] != null;
    }
    catch(_){
      return false;
    }
  }
}

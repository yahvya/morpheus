import 'dart:ui';

import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';
import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';

/// @brief Vérificateur de frame
class RecordCheck{
  /// @brief Liste des landmarks utiles
  /// @doc https://developers.google.com/ml-kit/vision/pose-detection?hl=fr
  final List<PoseLandmarkType> usefullLandmarks = [
    PoseLandmarkType.leftEye,
    PoseLandmarkType.rightEye,
    PoseLandmarkType.nose,
    PoseLandmarkType.leftEar,
    PoseLandmarkType.rightEar,
    PoseLandmarkType.leftMouth,
    PoseLandmarkType.rightMouth,
    PoseLandmarkType.leftEyeInner,
    PoseLandmarkType.leftEyeOuter,
    PoseLandmarkType.rightEyeOuter,
    PoseLandmarkType.rightEyeInner
  ];

  /// @brief Détecteur
  late PoseDetector detector;

  RecordCheck(){
    detector = PoseDetector(options: PoseDetectorOptions(
      model: PoseDetectionModel.accurate
    ));      
  }

  /// @brief Vérifie qu'un haut de corps est présent dans la frame
  /// @param camera controlleur de caméra
  /// @param frame frame
  /// @return Si un haut de corps est présent dans la frame
  Future<bool> check({required CameraController camera,required CameraImage frame}) async{
    try{
      var convertedImage = createImageFromFrame(camera.description, frame);

      if(convertedImage == null){
        return false;
      }

      List<Pose> results = await detector.processImage(convertedImage);

      // vérification de la présence d'un des landmarks dans la pause
      for(Pose pose in results){
        for(PoseLandmarkType usefullLandmark in usefullLandmarks){
          if(pose.landmarks.keys.contains(usefullLandmark)){
            return true;
          }
        }
      }

      return false;
    }
    catch(_){
      return false;
    }
  }

  /// @brief Converti la frame en InputImage
  /// @param camera la caméra
  /// @param frame la frame
  /// @return l'image convertie ou null en cas d'erreur
  InputImage? createImageFromFrame(CameraDescription camera,CameraImage frame) {
    final WriteBuffer allBytes = WriteBuffer();

    for (final Plane plane in frame.planes) {
      allBytes.putUint8List(plane.bytes);
    }

    final bytes = allBytes
      .done()
      .buffer
      .asUint8List();

    final Size imageSize = Size(frame.width.toDouble(), frame.height.toDouble());

    final imageRotation = InputImageRotationValue.fromRawValue(camera.sensorOrientation);

    if (imageRotation == null) return null;

    final inputImageFormat = InputImageFormatValue.fromRawValue(frame.format.raw);

    if (inputImageFormat == null) return null;

    final inputImageData = InputImageMetadata(
      size: imageSize,
      rotation: imageRotation,
      format: inputImageFormat,
      bytesPerRow: frame.planes[0].bytesPerRow,
    );

    return InputImage.fromBytes(bytes: bytes, metadata: inputImageData);
  }
}
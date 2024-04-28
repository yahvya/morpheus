import 'dart:ui';

import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';

/// @brief Classe de vérification du positionnement
abstract class Verifier{
  late FaceDetector detector;

  Verifier(){
    detector = new FaceDetector(
        options: new FaceDetectorOptions(
          enableContours: true
        )
    );
  }

  /// brief Vérifie si la position dans la frame correspond à la position attendue
  /// @param frame la frame vidéo à vérifier
  /// @return si la position dans la frame correspond à la position attendue
  Future<bool> verify(CameraDescription camera,CameraImage frame);

  /// @brief Converti la frame en InputImage
  InputImage? createImageFromFrame(CameraDescription camera,CameraImage image) {
    final WriteBuffer allBytes = WriteBuffer();

    for (final Plane plane in image.planes) {
      allBytes.putUint8List(plane.bytes);
    }

    final bytes = allBytes
        .done()
        .buffer
        .asUint8List();

    final Size imageSize = Size(
        image.width.toDouble(), image.height.toDouble());

    final imageRotation = InputImageRotationValue.fromRawValue(
        camera.sensorOrientation);

    if (imageRotation == null) return null;

    final inputImageFormat = InputImageFormatValue.fromRawValue(
        image.format.raw);

    if (inputImageFormat == null) return null;

    final inputImageData = InputImageMetadata(
      size: imageSize,
      rotation: imageRotation,
      format: inputImageFormat,
      bytesPerRow: image.planes[0].bytesPerRow,
    );

    return InputImage.fromBytes(bytes: bytes, metadata: inputImageData);
  }
}

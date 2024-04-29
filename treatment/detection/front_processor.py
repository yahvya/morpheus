##
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub
from typing import Any

import cv2
from cv2 import Mat
from fastapi import UploadFile
from numpy import ndarray, dtype, generic

from treatment.detection.detector import Detector
from treatment.exceptions.custom_exception import CustomException
import mediapipe

##
# @brief Gestionnaire de détection des points de la vidéo de face
class FrontProcessor:

    ##
    # @brief Extrait les données de la séquence vidéo de face
    # @param front_video vidéo de face avec ouverture de bouche
    @staticmethod
    def process(front_video: UploadFile):
        try:
            # traitement de la vidéo de face
            front_video_manager = cv2.VideoCapture(front_video.file.name)

            if not front_video_manager.isOpened():
                raise CustomException("Echec de traitement de la vidéo de face", True)

            # récupération de la distance maximale trouvée parmi les frames
            max_distance = -1

            while True:
                successfully_read, frame = front_video_manager.read()

                if not successfully_read:
                    break

                # normalisation de la frame
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                normalization_success, normalized_face_frame = FrontProcessor.get_normalized_face(rgb_frame)

                if not normalization_success:
                    continue

                # récupération de la distance bouche
                success, distance = FrontProcessor.get_mouth_distance(normalized_face_frame)

            if max_distance == -1:
                raise CustomException("Echec de détection de la bouche", True)

            front_video_manager.release()
        except CustomException as e:
            raise e
        except Exception:
            raise CustomException("Une erreur s'est produite lors du traitement des données", True)

    ##
    # @brief Trouve le visage dans la frame et le détoure puis le resize au format attendu
    # @param base_frame la frame de base
    # @param margin marge à ajouter autour du détourage
    # @return la frame normalisée avec l'état de succès au format (success, frame)
    @staticmethod
    def get_normalized_face(base_frame:  Mat | ndarray[Any, dtype[generic]] | ndarray, margin: int = 70) -> (bool, Mat | ndarray[Any, dtype[generic]] | ndarray | None):
        try:
            extractor = mediapipe.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

            founded_faces = extractor.process(base_frame)

            if not founded_faces.multi_face_landmarks:
                return False, None

            first_face_landmarks = founded_faces.multi_face_landmarks[0]

            # récupération du détourage du visage
            image_h, image_w, _ = base_frame.shape

            min_x, min_y = image_w, image_h
            max_x, max_y = 0, 0

            for landmark in first_face_landmarks.landmark:
                x = int(landmark.x * image_w)
                y = int(landmark.y * image_h)
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

            # détourage en ajoutant l'espace autour
            min_x = max(0, min_x - margin)
            min_y = max(0, min_y - margin)
            max_x = min(image_w, max_x + margin)
            max_y = min(image_h, max_y + margin)

            face_frame = base_frame[min_y:max_y, min_x:max_x]

            # redimensionnement de l'image

            return True, cv2.resize(face_frame, (200, 200), interpolation=cv2.INTER_AREA)
        except Exception:
            return False, None

    ##
    # @brief Calcule la distance entre le haut et le bas de la bouche
    # @param normalized_frame frame normalisé
    # @param mouth_landmarks_indexes index haut et bas recherchés
    # @param references_landmarks_indexes index yeux gauches et droits
    # @param reference_value valeur de référence
    # @return la distance avec l'état de succès au format (success, distance)
    @staticmethod
    def get_mouth_distance(normalized_frame: Mat | ndarray[Any, dtype[generic]] | ndarray, mouth_landmarks_indexes: (int, int) = (0, 17),references_landmarks_indexes: (int, int) = (133, 362)):
        try:
            extractor = mediapipe.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
            founded_faces = extractor.process(normalized_frame)

            if not founded_faces.multi_face_landmarks:
                return False, -1

            landmarks = founded_faces.multi_face_landmarks[0].landmark

            up_index, down_index = mouth_landmarks_indexes

            # récupération des points des index recherchés
            if not max(up_index, down_index) < len(landmarks):
                return False, -1

            up_landmark = landmarks[up_index]
            down_landmark = landmarks[down_index]

            # calcul de la distance
            distance_in_pixels = Detector.get_distance_between_landmarks_in_pixel(up_landmark, down_landmark, normalized_frame.shape)
            success, value = Detector.get_pixel_reference_value(landmarks, references_landmarks_indexes, normalized_frame.shape, 3.2)

            print(f"p : {distance_in_pixels} - value : {value} - result: {distance_in_pixels * value}")

            return success, distance_in_pixels * value if success else -1
        except Exception:
            return False, -1



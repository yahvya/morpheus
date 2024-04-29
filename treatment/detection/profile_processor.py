##
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from enum import Enum
import cv2
import mediapipe
from fastapi import UploadFile
from treatment.exceptions.custom_exception import CustomException


##
# @brief Définition du type de profile
class ProfileSide(Enum):
    ##
    # @brief Profil gauche
    LEFT = 1
    ##
    # @brief Profil droit
    RIGHT = 2


##
# @brief Gestionnaire de détection des points des vidéos de profil
class ProfileProcessor:
    ##
    # @brief Extrait les données des vidéos de profil (pointe du menton, tragus (point à côté de l'oreille), bout de la machoire)
    # @param video la vidéo à traiter
    # @param side le côté de profil
    # @return les données extraites
    @staticmethod
    def process(video: UploadFile, side: ProfileSide):
        try:
            # traitement de la vidéo de profil
            video_manager = cv2.VideoCapture(video.file.name)

            if not video_manager.isOpened():
                raise CustomException("Echec de traitement de la vidéo de face", True)

            while True:
                successfully_read, frame = video_manager.read()

                if not successfully_read:
                    break

                success, datas = ProfileProcessor.extract_profile_frame_datas(frame)
        except CustomException as e:
            raise e
        except Exception:
            raise CustomException("Une erreur s'est produite lors du traitement des données", True)

    @staticmethod
    def extract_profile_frame_datas(frame):
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # récupération du visage
            extractor = mediapipe.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                                               min_detection_confidence=0.5,
                                                               min_tracking_confidence=0.5)

            founded_faces = extractor.process(frame)

            if not founded_faces.multi_face_landmarks:
                return False, None

            result = {}

            first_face_landmarks = founded_faces.multi_face_landmarks[0]

            # récupération de la position du menton
            result["chin"] = {
                "landmark": first_face_landmarks.landmark[377],
                "shape": frame.shape
            }

            return True, result
        except Exception:
            return False, None

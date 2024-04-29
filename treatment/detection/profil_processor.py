##
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from enum import Enum
import cv2
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
    # @brief Extrait les données des vidéos de profil 
    @staticmethod
    def process(video: UploadFile,side: ProfileSide):
        try:
            # traitement de la vidéo de profil
            video_manager = cv2.VideoCapture(video.file.name)

            if not video_manager.isOpened():
                raise CustomException("Echec de traitement de la vidéo de face", True)

            while True:
                successfully_read, frame = video_manager.read()

                if not successfully_read:
                    break
                
            

                
        except CustomException as e:    
            raise e
        except Exception:
            raise CustomException("Une erreur s'est produite lors du traitement des données", True)
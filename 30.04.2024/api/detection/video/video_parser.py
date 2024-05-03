import cv2
from mediapipe import solutions
from detection.video.parser_result import ParserResult
from api_utils.utils import CustomException
from typing import List, Callable

"""
    @brief Parseur de vidéo
"""
class VideoParser:
    """
        @brief Parse la vidéo fournie
        @param video_path chemin de la vidéo à lire
        @param important_landmarks liste des landmarks important à récupérer. Si vide tous les landmarks seront traités
        @param custom_detection_functions Fonctions customisés de détection. Prennent en paramètre (frame,frame_count, important_landmarks) et fourni en résultat une map indicé par un landmark et avec comme valeur les coordonnées en pixel sur la frame 
        @return résultats du parsing
        @throws CustomException en cas d'erreur
    """
    @staticmethod
    def parse(
        video_path: str, 
        important_landmarks: List[int] = [], 
        custom_detection_functions: List[Callable] = []
    ) -> ParserResult:
        try:        

            return ParserResult()
        except CustomException as e:
            raise e
        except:
            raise CustomException(message= "Une erreur s'est produite lors du traitement de la vidéo")
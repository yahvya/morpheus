import cv2
from numpy import dtype, generic, ndarray
from detection.utils.utils import new_face_detector
from detection.video.parser_result import ParserResult
from api_utils.utils import CustomException
from typing import Any, List, Callable

"""
    @brief Parseur de vidéo
"""
class VideoParser:
    """
        @param video_path chemin de la vidéo à lire
    """
    def __init__(
        self,
        video_path: str
    ) -> None:
        self.video_path = video_path

    """
        @brief Parse la vidéo fournie
        @param important_landmarks liste des index des points important à récupérer
        @param custom_detection_functions Fonctions customisés de détection. Prennent en paramètre (frame,frame_counter, important_landmarks) et fourni en résultat une map indicé par un landmark et avec comme valeur les données sur la récupération dict[int,dict[str,]]
        @return résultats du parsing
        @throws CustomException en cas d'erreur
    """
    def parse(
        self,
        important_landmarks: List[int] = [], 
        custom_detections_functions: List[Callable] = []
    ) -> ParserResult:
        video = None

        try:        
            video = cv2.VideoCapture(filename= self.video_path)
            
            if not video.isOpened():
                raise CustomException(message= "Echec de traitement de la vidéo")

            self.face_detector = new_face_detector()

            result = ParserResult()
            frame_counter = 0

            """
                lecture et traitement de la vidéo par extraction des points 
            """
            while True:
                successfuly_read, frame = video.read()

                if not successfuly_read:
                    break

                frame_counter += 1

                """  
                    Extraction des landmarks via facemesh
                """
                important_landmarks_datas_in_frame = self._extract_important_points(
                    frame_counter= frame_counter,
                    frame= frame,
                    important_landmarks= important_landmarks
                )

                """
                    Extractions customisés et fusion avec les détections facemesh
                """
                custom_detections_result = [
                    custom_detector(frame, frame_counter, important_landmarks)
                    for custom_detector in custom_detections_functions
                ]
                
                custom_detections_result.append(important_landmarks_datas_in_frame)

            video.release()

            return result
        except CustomException as e:
            if video != None and video.isOpened():
                video.release()

            raise e
        except:
            if video != None and video.isOpened():
                video.release()

            raise CustomException(message= "Une erreur s'est produite lors du traitement de la vidéo")

    """
        @brief Extrait les points important
        @param frame_counter compteur contenant le numéro de la frame
        @param important_landmarks liste des index des points important
        @attention Attend que le détecteur interne ai été initialisé 
        @return map des détections faîtes
    """
    def _extract_important_points(
            self,
            frame_counter:int, 
            frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray, 
            important_landmarks: List[int]
        ) -> dict[int,dict[str,]]:
        if  len(important_landmarks) == 0:
            return {}
        
        return {}
    

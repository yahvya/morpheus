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
        @param custom_detection_functions Fonctions customisés de détection. Prennent en paramètre (frame, important_landmarks) et fourni en résultat une map indicé par un landmark et avec comme valeur les données sur la récupération dict[int,dict[str,]]
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
                    frame= frame,
                    important_landmarks= important_landmarks
                )

                """
                    Extractions customisés et fusion avec les détections facemesh
                """
                custom_detections_result = [
                    custom_detector(frame, important_landmarks)
                    for custom_detector in custom_detections_functions
                ]
                
                custom_detections_result.append(important_landmarks_datas_in_frame)

                """
                    ajout des données de détections parmis les résultats
                """
                for ways_results in custom_detections_result:
                    for landmark_index in ways_results:
                        result.add_frame_data(
                            frame_counter= frame_counter,
                            landmark= landmark_index,
                            datas= ways_results[landmark_index]
                        )
                    
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
        @param important_landmarks liste des index des points important
        @attention Attend que le détecteur interne ai été initialisé 
        @return map des détections faîtes
    """
    def _extract_important_points(
            self,
            frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray, 
            important_landmarks: List[int]
        ) -> dict[int,dict[str,int]]:
        try:
            if len(important_landmarks) == 0:
                return {}

            """
                Conversion de la frame en rgb et récupération des visages détectés
            """
            converted_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) 

            founded_faces = self.face_detector.process(converted_frame)

            if not founded_faces.multi_face_landmarks:
                return {}


            """
                Récupération des coordonnées des points attendus
            """ 
            founded_face_landmarks = founded_faces.multi_face_landmarks[0].landmark
            founded_face_landmarks_len = len(founded_face_landmarks)
            image_height, image_width, _ = converted_frame.shape
            result_map = {}   

            for landmark_index in important_landmarks:
                if landmark_index >= founded_face_landmarks_len:
                    continue

                founded_landmark = founded_face_landmarks[landmark_index]

                result_map[landmark_index] = {
                    "x": int(founded_landmark.x * image_width),
                    "y": int(founded_landmark.y * image_height)
                }

            return result_map
        except:
            return {}
    

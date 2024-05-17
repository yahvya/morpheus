import os
import time
import cv2
from numpy import dtype, generic, ndarray
from detection.treatment.head_move_treatment import HeadMoveTreatment
from detection.treatment.jaw_treatment import JawTreatment
from detection.treatment.mouth_treatment import MouthTreatment
from detection.treatment.treatment_result import TreatmentResult
from detection.utils.utils import new_face_detector
from detection.video.parser_result import ParserResult
from api_utils.utils import CustomException
from typing import Any, List, Callable

recap_dir = f"{os.path.dirname(__file__)}/resources/recaps/" 

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
        @brief Parse la vidéo fournie et la traite
        @param important_landmarks liste des index des points important à récupérer
        @param custom_detection_functions Fonctions customisés de détection. Prennent en paramètre (frame, important_landmarks, important_landmarks_datas_in_frame) et fourni en résultat une map indicé par un landmark et avec comme valeur les données sur la récupération dict[int,dict[str,]]
        @return résultats du traitement
        @throws CustomException en cas d'erreur
    """
    def parse(
        self,
        important_landmarks: List[int] = [], 
        custom_detections_functions: List[Callable] = []
    ) -> TreatmentResult:
        video = None
        file_name = f"{int(time.time())}.mp4"
        recap_video_path = f"{recap_dir}{file_name}"
        recap_video = None

        try:        
            video = cv2.VideoCapture(filename= self.video_path)
            
            if not video.isOpened():
                raise CustomException(message= "Echec de traitement de la vidéo")
            
            """
                création du fichier de vidéo recap
            """
            recap_video = cv2.VideoWriter(
                filename= recap_video_path,
                fourcc= cv2.VideoWriter_fourcc(*"H264"),
                fps= video.get(propId= cv2.CAP_PROP_FPS),
                frameSize= (
                    int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                )
            )

            """
                Création des utilitaires de traitement
            """

            parser_result = ParserResult()
            
            mouth_treatment_manager = MouthTreatment(
                parsing_result= parser_result,
                drawing_color= [255,0,0]
            )

            head_move_treatment_manager = HeadMoveTreatment(
                parsing_result= parser_result,
                drawing_color= [142,35,42]
            )

            jaw_treatment_manager = JawTreatment(
                parsing_result= parser_result,
                drawing_color= [0,255,0]
            )

            self.face_detector = new_face_detector()

            frame_counter = 0
            tmp = {
                "head-move-datas": [],
                "jaw-datas": [],
                "mouth-max-distance": 0
            }

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
                    custom_detector(frame, important_landmarks, important_landmarks_datas_in_frame)
                    for custom_detector in custom_detections_functions
                ]
                
                custom_detections_result.append(important_landmarks_datas_in_frame)

                """
                    ajout des données de détections parmis les résultats
                """
                for ways_results in custom_detections_result:
                    for landmark_index in ways_results:
                        parser_result.add_frame_data(
                            frame_counter= frame_counter,
                            landmark= landmark_index,
                            datas= ways_results[landmark_index]
                        )

                """
                    Création de la frame de dessin
                """
                drawable_frame = frame.copy()

                """
                    Traitement de la distance d'ouverture de bouche
                """
                success, mouth_distance = mouth_treatment_manager.extract_mouth_distance(
                    frame_counter= frame_counter,
                    drawable_frame= drawable_frame
                )   

                if success and mouth_distance > tmp["mouth-max-distance"]:
                    tmp["mouth-max-distance"] = mouth_distance

                """
                    Traitement du basculement de ma tête
                """
                success, head_move_datas = head_move_treatment_manager.extract_head_move_datas(
                    frame_counter= frame_counter,
                    drawable_frame= drawable_frame
                )

                if success:
                    tmp["head-move-datas"].append(head_move_datas)

                """
                    Traitement des données de la machoire 
                """
                success, jaw_datas = jaw_treatment_manager.extract_jaw_datas(
                    frame_counter= frame_counter,
                    drawable_frame= drawable_frame
                )

                if success:
                    tmp["jaw-datas"].append(jaw_datas)

                recap_video.write(image= drawable_frame)

            """
                Libération des ressources
            """
            video.release()
            recap_video.release()

            """
                Création et remplissage de l'objet résultat
            """
            treatment_result = TreatmentResult()

            treatment_result.set_max_mouth_distance(max_mouth_distance= tmp["mouth-max-distance"])
            treatment_result.set_recap_video_path(recap_video_path= file_name)
            treatment_result.set_parse_result(parse_result= parser_result)

            return treatment_result
        except CustomException as e:
            if video != None and video.isOpened():
                video.release()

            if recap_video != None:
                recap_video.release()

            if os.path.exists(path= recap_video_path):
                os.unlink(path= recap_video_path)

            raise e
        except:
            if video != None and video.isOpened():
                video.release()

            if recap_video != None:
                recap_video.release()

            if os.path.exists(path= recap_video_path):
                os.unlink(path= recap_video_path)

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
                if landmark_index >= founded_face_landmarks_len or founded_face_landmarks[landmark_index] is None:
                    continue

                founded_landmark = founded_face_landmarks[landmark_index]
                
                result_map[landmark_index] = {
                    "x": int(founded_landmark.x * image_width),
                    "y": int(founded_landmark.y * image_height),
                    "z": int(founded_landmark.z)
                }

            return result_map
        except:
            return {}


import cv2
import time
import os
from math import pow, sqrt
from typing import Any, Tuple
from numpy import dtype, generic, ndarray
from detection.video.parser_result import ParserResult
from api_utils.utils import CustomException
from detection.treatment.mouth_treatment import MouthTreatment

"""
    @brief Traiteur des informations vidéos
"""
class Treatment:
    """
        @param video_path chemin de la vidéo de base à traiter
        @param parsing_result résultat de parsing
        @param drawing_color couleur des dessins
    """
    def __init__(
        self, 
        video_path: str, 
        parsing_result: ParserResult,
        drawing_color: Tuple[int, int, int] = [165,62,239]
    ):
        self.parsing_result = parsing_result
        self.video_path = video_path
        self.drawing_color = drawing_color

    """
        @brief Lance le traitement des résultats
        @return les données de traitements en plus du chemin de la vidéo récaptifulative
        @throws CustomException en cas d'erreur
    """
    def treat_results(self) -> dict[str,any]:
        recap_video_path = f"{os.path.dirname(__file__)}/resources/recaps/{int(time.time())}.mp4"
        video = None 
        recap_video = None

        try:
            """
                Ouverture de la vidéo et création du fichier de vidéo recap
            """
            video = cv2.VideoCapture(filename= self.video_path)

            if not video.isOpened():
                raise Exception()
            
            recap_video = cv2.VideoWriter(
                filename= recap_video_path,
                fourcc= cv2.VideoWriter_fourcc(*"MP4V"),
                fps= video.get(propId= cv2.CAP_PROP_FPS),
                frameSize= (
                    int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                )
            )
            
            mouth_treatment_manager = MouthTreatment(
                parsing_result= self.parsing_result,
                drawing_color= self.drawing_color
            )

            frame_counter = 0
            result  = {
                "mouth-max-distance": 0
            }
            
            """
                Création de la vidéo recap et extraction des données
            """
            while True:
                successfuly_read, frame = video.read()

                if not successfuly_read:
                    break

                """
                    Création de la frame de dessin
                """
                drawable_frame = frame.copy()
                frame_counter += 1

                """
                    Traitement de la distance d'ouverture de bouche
                """
                success, mouth_distance = mouth_treatment_manager.extract_mouth_distance(
                    frame_counter= frame_counter,
                    drawable_frame= drawable_frame
                )   

                if success and mouth_distance > result["mouth-max-distance"]:
                    result["mouth-max-distance"] = mouth_distance

                recap_video.write(image= drawable_frame)

            """
                Libération des ressources et ajout de la vidéo recap au résultat
            """
            video.release()
            recap_video.release()

            result["recap-video"] = recap_video_path

            return result
        except CustomException as e:
            if os.path.exists(path= recap_video_path):
                os.unlink(path= recap_video_path)

            if video != None:
                video.release()

            if recap_video != None:
                recap_video.release()

            raise e
        except:
            if os.path.exists(path= recap_video_path):
                os.unlink(path= recap_video_path)

            if video != None:
                video.release()

            if recap_video != None:
                recap_video.release()

            raise CustomException(message= "Une erreur s'est produite lors du traitement des données extraites")

    """
        @brief Dessine le point sur la frame fournie
        @param drawable_frame frame de dessin
        @param landmark données du point à dessiner
        @param drawing_color couleur du dessin
    """
    @staticmethod
    def draw_landmark_on(
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
        landmark: dict[str,any],
        drawing_color: Tuple[int, int, int]
    ):
        cv2.circle(
            img= drawable_frame,
            center= (landmark["datas"]["x"], landmark["datas"]["y"]),
            radius= 5,
            color= drawing_color,
            thickness= -1
        )

    """
        @brief Dessine le point sur la frame fournie
        @param drawable_frame frame de dessin
        @param landmark_one données du premier point à dessiner
        @param landmark_two données du second point à dessiner
        @param drawing_color couleur du dessin
    """
    @staticmethod
    def draw_line_between(
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
        landmark_one: dict[str,any],
        landmark_two: dict[str,any],
        drawing_color: Tuple[int, int, int]
    ):
        cv2.line(
            img= drawable_frame,
            pt1= (landmark_one["datas"]["x"], landmark_one["datas"]["y"]),
            pt2= (landmark_two["datas"]["x"], landmark_two["datas"]["y"]),
            color= drawing_color,
            thickness= 4
        )

    """
        @brief Calcul l'équavlence entre pixel et centimètre
        @param reference_landmark données du référenciel
        @param real_value valeur attendue
        @return la valeur de référence
    """
    @staticmethod
    def get_a_pixel_value_in_centimer(reference_landmark: dict[str,int|float], real_value:int) -> int|float:
        return reference_landmark["radius"] / real_value
    

    """
        @brief Calcule la distance en pixel entre les deux points fournis
        @param landmark_one point 1
        @param landmark_two point 2
        @return La distance en pixel
    """
    @staticmethod
    def calculate_pixel_distance_between(landmark_one: dict[str,any],landmark_two: dict[str,any]) -> int |float:
        landmark_one_coords = landmark_one["datas"]
        landmark_two_coords = landmark_two["datas"]

        return sqrt(
            pow(landmark_one_coords["x"] - landmark_two_coords["x"],2) +
            pow(landmark_one_coords["y"] - landmark_two_coords["y"],2)
        )
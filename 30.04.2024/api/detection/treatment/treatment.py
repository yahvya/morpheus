import cv2
import time
import os
from math import pow, sqrt
from typing import Any, Tuple
from numpy import dtype, generic, ndarray
from detection.treatment.jaw_treatment import JawTreatment
from detection.treatment.head_move_treatment import HeadMoveTreatment
from detection.video.parser_result import ParserResult
from api_utils.utils import CustomException
from detection.treatment.mouth_treatment import MouthTreatment
from detection.treatment.treatment_result import TreatmentResult

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
        parsing_result: ParserResult
    ):
        self.parsing_result = parsing_result
        self.video_path = video_path

    """
        @brief Lance le traitement des résultats
        @return les résultats du traitement
        @throws CustomException en cas d'erreur
    """
    def treat_results(self) -> TreatmentResult:
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

            """
                Création des utilitaires de traitement
            """
            
            mouth_treatment_manager = MouthTreatment(
                parsing_result= self.parsing_result,
                drawing_color= [165,62,239]
            )

            head_move_treatment_manager = HeadMoveTreatment(
                parsing_result= self.parsing_result,
                drawing_color= [142,35,42]
            )

            jaw_treatment_manager = JawTreatment(
                parsing_result= self.parsing_result,
                drawing_color= [0,255,0]
            )

            frame_counter = 0
            result  = {
                "mouth-max-distance": 0
            }
            tmp = {
                "head-move-datas": [],
                "jaw-datas": []
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
                Libération des ressources et ajout de la vidéo recap au résultat
            """
            video.release()
            recap_video.release()
            
            """
                Création et remplissage de l'objet résultat
            """
            treatment_result = TreatmentResult()

            treatment_result.set_max_mouth_distance(max_mouth_distance= result["mouth-max-distance"])
            treatment_result.set_recap_video_path(recap_video_path= recap_video_path)

            return treatment_result
        except CustomException as e:
            if video != None:
                video.release()

            if recap_video != None:
                recap_video.release()

            if os.path.exists(path= recap_video_path):
                os.unlink(path= recap_video_path)

            raise e
        except:
            if video != None:
                video.release()

            if recap_video != None:
                recap_video.release()

            if os.path.exists(path= recap_video_path):
                os.unlink(path= recap_video_path)

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
            radius= landmark["datas"]["radius"] if "radius" in landmark["datas"] else 5,
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
        @brief Dessine le texte à côté du point fourni
        @param drawable_frame frame de dessin
        @param landmark landmark à côté duquel dessiner
        @param text message
        @param drawing_color couleur de dessin
    """
    @staticmethod
    def draw_text_near(
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
        landmark: dict[str,any],
        text: str,
        drawing_color: Tuple[int, int, int]
    ):
        cv2.putText(
            img= drawable_frame,
            text= text,
            org= (landmark["datas"]["x"],landmark["datas"]["y"]),
            fontFace= cv2.FONT_HERSHEY_COMPLEX,
            fontScale= 3,
            color= drawing_color
        )

    """
        @brief Calcul l'équavlence entre pixel et centimètre
        @param reference_landmark données du référenciel
        @param real_value valeur attendue
        @return la valeur de référence
    """
    @staticmethod
    def get_a_pixel_value_in_centimer(reference_landmark: dict[str,int|float], real_value:int) -> int|float:
        return reference_landmark["datas"]["radius"] / real_value

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

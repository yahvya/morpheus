import cv2
from numpy import dtype, generic, ndarray
from detection.utils.important_landmarks import ImportantLandmarks, MarkerImportLandmarks
from detection.video.parser_result import ParserResult
from typing import Any, Tuple

"""
    @brief Gestionnaire des séquences levés et baissés de tête
"""
class HeadMoveTreatment:
    """
        @param parsing_result résultat de parsing
        @param drawing_color couleur des dessins
    """
    def __init__(
        self, 
        parsing_result: ParserResult,
        drawing_color: Tuple[int, int, int] = [165,62,239]
    ):
        self.parsing_result = parsing_result
        self.drawing_color = drawing_color
    
    """
        @brief Extrait les données du mouvement de tête levé baissé de profil droit
        @param frame_counter numéro de frame
        @param drawable_frame frame de dessin recap
    """
    def extract_head_move_datas(
        self,
        frame_counter:int,
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray
    ) -> Tuple[bool,Any|None]:
        from detection.treatment.treatment import Treatment

        try:
            """
                Récupération et dessin du point du menton
            """
            chin_landmark = self.parsing_result.get_landmark_datas_for_frame(
                landmark= ImportantLandmarks.CHIN_CENTER.value,
                frame_counter= frame_counter
            )

            if chin_landmark != None:
                Treatment.draw_landmark_on(
                    drawable_frame= drawable_frame,
                    landmark= chin_landmark,
                    drawing_color= self.drawing_color
                )
            
            """
                Récupération et dessin du marqueur sur le cou
            """
            neck_marker = self.parsing_result.get_landmark_datas_for_frame(
                landmark= MarkerImportLandmarks.ADAM_APPLE.value,
                frame_counter= frame_counter
            )

            if neck_marker == None:
                return False, None
            
            Treatment.draw_landmark_on(
                drawable_frame= drawable_frame,
                landmark= neck_marker,
                drawing_color= self.drawing_color
            )

            if chin_landmark == None:
                return False, None
            
            Treatment.draw_line_between(
                drawable_frame= drawable_frame,
                landmark_one= neck_marker,
                landmark_two= chin_landmark,
                drawing_color= self.drawing_color
            )

            return True, {
                "chin": chin_landmark,
                "neck": neck_marker
            }
        except:
            return False, None

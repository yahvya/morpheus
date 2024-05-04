import cv2
from typing import Any, Tuple
from numpy import dtype, generic, ndarray
from detection.video.parser_result import ParserResult
from detection.utils.important_landmarks import ImportantLandmarks, MarkerImportLandmarks

"""
    @brief Gestionnaire des données de la bouche
"""
class MouthTreatment:
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
        @brief Extrait la distance de la bouche sur la frame fournie
        @param frame_counter numéro de frame
        @param drawable_frame frame de dessin recap
        @return tuple avec premier paramètre booléen indiquant le succès et second contenant la distance ou None en fonction du succès
    """
    def extract_mouth_distance(
        self,
        frame_counter:int,
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray
    ) -> Tuple[bool,int|None]:
        from detection.treatment.treatment import Treatment

        try:
            """
                Récupération des landmarks et dessin de ceux trouvés
            """

            upper_landmark = self.parsing_result.get_landmark_datas_for_frame(
                landmark= ImportantLandmarks.UPPER_LIP.value,
                frame_counter= frame_counter
            )

            if upper_landmark != None:
                Treatment.draw_landmark_on(
                    drawable_frame= drawable_frame,
                    landmark= upper_landmark,
                    drawing_color= self.drawing_color
                )

            lower_landmark = self.parsing_result.get_landmark_datas_for_frame(
                landmark= ImportantLandmarks.LOWER_LIP.value,
                frame_counter= frame_counter
            )

            if lower_landmark == None:
                return False, None
            
            Treatment.draw_landmark_on(
                drawable_frame= drawable_frame,
                landmark= lower_landmark,
                drawing_color= self.drawing_color
            )

            if upper_landmark == None:
                return False, None

            Treatment.draw_line_between(
                drawable_frame= drawable_frame,
                landmark_one= upper_landmark,
                landmark_two= lower_landmark,
                drawing_color= self.drawing_color
            )

            """
                Calcul de la distance entre les deux points en utilisant comme valeur de référence le sticker de référence frontal
            """
            

            return True, 30
        except:
            return False, None
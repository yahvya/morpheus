from typing import Any, Tuple

import cv2
from numpy import dtype, generic, ndarray
from detection.utils.important_landmarks import ImportantLandmarks
from detection.video.parser_result import ParserResult

"""
    @brief Extraction des points de la machoire
"""
class JawTreatment:
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
        @brief Extrait les données de la machoire avec le point gauche droit et menton
        @param frame_counter numéro de frame
        @param drawable_frame frame de dessin recap
    """
    def extract_jaw_datas(
        self,
        frame_counter:int,
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray
    ) -> Tuple[bool,dict[str,any]]:
        from detection.treatment.treatment import Treatment

        try:
            """
                Récupération du point du menton et dessin
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
                Récupération du point de la machoire gauche et dessin
            """
            left_jaw_landmark = self.parsing_result.get_landmark_datas_for_frame(
                landmark= ImportantLandmarks.LEFT_JAW.value,
                frame_counter= frame_counter
            )

            if left_jaw_landmark != None:
                Treatment.draw_landmark_on(
                    drawable_frame= drawable_frame,
                    landmark= left_jaw_landmark,
                    drawing_color= self.drawing_color
                )

                if chin_landmark != None:
                    Treatment.draw_line_between(
                        drawable_frame= drawable_frame,
                        landmark_one= left_jaw_landmark,
                        landmark_two= chin_landmark,
                        drawing_color= self.drawing_color
                    )

            """
                Récupération du point de la machoire droite et dessin
            """
            right_jaw_landmark = self.parsing_result.get_landmark_datas_for_frame(
                landmark= ImportantLandmarks.RIGHT_JAW.value,
                frame_counter= frame_counter
            )

            if right_jaw_landmark != None:
                Treatment.draw_landmark_on(
                    drawable_frame= drawable_frame,
                    landmark= right_jaw_landmark,
                    drawing_color= self.drawing_color
                )

                if chin_landmark != None:
                    Treatment.draw_line_between(
                        drawable_frame= drawable_frame,
                        landmark_one= right_jaw_landmark,
                        landmark_two= chin_landmark,
                        drawing_color= self.drawing_color
                    )

            if not (None in [right_jaw_landmark, left_jaw_landmark]):
                Treatment.draw_line_between(
                    drawable_frame= drawable_frame,
                    landmark_one= right_jaw_landmark,
                    landmark_two= left_jaw_landmark,
                    drawing_color= self.drawing_color
                )

            if None in [right_jaw_landmark, left_jaw_landmark, chin_landmark]:
                return False, None

            return True, {
                "left_jaw": left_jaw_landmark,
                "right_jaw": right_jaw_landmark,
                "chin": chin_landmark
            }
        except:
            return False, None
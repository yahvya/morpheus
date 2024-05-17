import cv2
from typing import Any, Tuple
from numpy import dtype, generic, ndarray
from detection.utils.important_landmarks import ImportantLandmarks, MarkerImportLandmarks
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
                Récupération du tragus droit
            """
            right_tragus = self.parsing_result.get_landmark_datas_for_frame(
                landmark= ImportantLandmarks.RIGHT_TRAGUS.value,
                frame_counter= frame_counter
            )

            if right_tragus != None:
                Treatment.draw_landmark_on(
                    drawable_frame= drawable_frame,
                    landmark= right_tragus,
                    drawing_color= self.drawing_color
                )

            """
                Récupération du tragus gauche
            """
            left_tragus = self.parsing_result.get_landmark_datas_for_frame(
                landmark= ImportantLandmarks.LEFT_TRAGUS.value,
                frame_counter= frame_counter
            )

            if left_tragus != None:
                Treatment.draw_landmark_on(
                    drawable_frame= drawable_frame,
                    landmark= left_tragus,
                    drawing_color= self.drawing_color
                )

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

                """
                    Récupération du point de référence frontal et calcul de la distance entre les deux points
                """
                front_reference_marker = self.parsing_result.get_landmark_datas_for_frame(
                    landmark= MarkerImportLandmarks.FRONT_REFERENCE.value,
                    frame_counter= frame_counter
                )

                if front_reference_marker == None:
                    return False, None
                
                centimeter_reference = Treatment.get_a_pixel_value_in_centimer(
                    reference_landmark= front_reference_marker,
                    real_value= 0.4
                )

                distance_in_pixel = Treatment.calculate_pixel_distance_between(
                    landmark_one= left_jaw_landmark,
                    landmark_two= right_jaw_landmark
                )

                distance = round(distance_in_pixel / centimeter_reference,2)

                Treatment.draw_text_near(
                    drawable_frame= drawable_frame,
                    landmark= left_jaw_landmark,
                    text= f"{distance} cm",
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

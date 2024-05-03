import cv2
from detection.video.parser_result import ParserResult
from api_utils.utils import CustomException

"""
    @brief Traiteur des informations vidéos
"""
class Treatment:
    """
        @param video_path chemin de la vidéo de base à traiter
        @param parsing_result résultat de parsing
    """
    def __init__(self, video_path: str, parsing_result: ParserResult):
        self.parsing_result = parsing_result
        self.video_path = video_path

    """
        @brief Lance le traitement des résultats
        @return les données de traitements en plus du chemin de la vidéo récaptifulative
        @throws CustomException en cas d'erreur
    """
    def treat_results(self) -> dict[str,any]:
        try:
            video = cv2.VideoCapture(filename= self.video_path)

            if not video.isOpened():
                raise Exception()
            
            frame_counter = 0
            
            while True:
                successfuly_read, frame = video.read()

                if not successfuly_read:
                    break

                frame_counter += 1

        
        except CustomException as e:
            raise e
        except:
            raise CustomException(message= "Une erreur s'est produite lors du traitement des données extraites")
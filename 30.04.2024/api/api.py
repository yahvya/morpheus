"""
    @brief Api morpheus
"""

import os
from time import time
from fastapi import FastAPI, File, Header, UploadFile, Form
from api_utils.utils import CustomException, check_signature, temporary_upload
from detection.video.video_parser import VideoParser
from detection.utils.important_landmarks import ImportantLandmarks
from detection.utils.marker_detection import detect_neck_marker, detect_front_reference_marker, detect_left_profile_marker, detect_right_profile_marker
from detection.treatment.treatment import Treatment

app = FastAPI()

"""
    @brief Crée le format d'affichage en fonction du timestamp fourni
    @param timestamp le timestamp
    @return Temps affichable
"""
def format_timestamp(timestamp: float|int) -> str:
    return ""

"""
    @brief Traitement de vidéo
"""
@app.post("/morpheus-mobile")
async def manage_mobile_app_request(
    signature: str = Header(...),
    video: UploadFile = File(...),
    mallampati_score: int = Form(...),
    mobility_grade_score: int = Form(...),
    username: str = Form(...),
    user_email: str = Form(...)
):
    file_path = None

    try:
        # vérification de la signature
        # check_signature(signature= signature)
        
        # création de la sauvegarde temporaire
        file_path = temporary_upload(file= video)

        # parsing de la vidéo
        parsing_start_time = time()
        parsing_result = VideoParser(video_path= file_path).parse(
            # important_landmarks= [landmark.value for landmark in ImportantLandmarks],
            important_landmarks= [ImportantLandmarks.UPPER_LIP.value,ImportantLandmarks.LOWER_LIP.value],
            # custom_detections_functions= [detect_neck_marker,detect_right_profile_marker, detect_left_profile_marker, detect_front_reference_marker]
            custom_detections_functions= [detect_front_reference_marker]
        )
        parsing_end_time = time()

        # traitement des extracations et création de la vidéo recap
        treatment_start_time = time()
        treatment_result = Treatment(
            video_path= file_path,
            parsing_result= parsing_result
        ).treat_results()
        treatment_end_time = time()

        # suppression du fichier
        os.unlink(path= file_path)

        return {
            "success": False,
            "error": "Erreur de test"
        }

        return {
            "success": True,
            "datas": {
                "textualDatas": {
                    "Temps d'extraction des données": format_timestamp(timestamp= parsing_end_time - parsing_start_time),
                    "Temps de traitement et génération de vidéo": format_timestamp(timestamp= treatment_end_time - treatment_start_time)
                }
            }
        }
    except CustomException as e:
        if file_path != None:
            os.unlink(path= file_path)

        return {
            "success": False,
            "error": e.get_error_message()
        }
    except:
        if file_path != None:
            os.unlink(path= file_path)
            
        return {
            "success": False,
            "error": "Une erreur s'est produite sur le serveur"
        }

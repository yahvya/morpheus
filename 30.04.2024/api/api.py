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
from datetime import timedelta

app = FastAPI()

"""
    @brief Crée une durée affichable à partir d'un time de départ et de fin
    @param start time de départ
    @param end time de fin
    @return Durée affichable
"""
def time_from_diff_of(start: float|int, end: float|int) -> str:
    duration = end - start
    duration_timedelta = timedelta(seconds=duration)

    return str(duration_timedelta)

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
            important_landmarks= [landmark.value for landmark in ImportantLandmarks],
            custom_detections_functions= [detect_neck_marker,detect_right_profile_marker, detect_left_profile_marker, detect_front_reference_marker]
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
            "success": True,
            "datas": {
                "recap-video-get-link": "",
                "textualDatas": {
                    "Temps d'extraction des données": time_from_diff_of(
                        start= parsing_start_time,
                        end= parsing_end_time
                    ),
                    "Temps de traitement et génération de vidéo": time_from_diff_of(
                        start= treatment_start_time,
                        end= treatment_end_time
                    ),
                    "Distance maximale d'ouverture de bouche": treatment_result.get_max_mouth_distance()
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

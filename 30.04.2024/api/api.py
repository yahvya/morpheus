"""
    @brief Api morpheus
"""

import os
from fastapi import FastAPI, File, Header, UploadFile, Form
from api_utils.utils import CustomException, check_signature, temporary_upload
from detection.video.video_parser import VideoParser
from detection.utils.important_landmarks import ImportantLandmarks
from detection.utils.marker_detection import detect_neck_marker, detect_front_reference_marker, detect_left_profile_marker, detect_right_profile_marker
from detection.treatment.treatment import Treatment

app = FastAPI()

"""
    @brief Traitement de vidéo
"""
@app.post("/morpheus-mobile")
async def manage_mobile_app_request(
    signature: str = Header(...),
    video: UploadFile = File(...),
    mallampatiScore: int = Form(...),
    username: str = Form(...),
    user_email: str = Form(...)
):
    file_path = None

    try:
        # vérification de la signature
        check_signature(signature= signature)
        
        # création de la sauvegarde temporaire
        file_path = temporary_upload(file= video)

        # traitement de la vidéo
        parsing_result = VideoParser(video_path= file_path).parse(
            important_landmarks= [landmark.value for landmark in ImportantLandmarks],
            custom_detections_functions= [detect_neck_marker,detect_right_profile_marker, detect_left_profile_marker, detect_front_reference_marker]
        )

        treatment_result = Treatment(
            video_path= file_path,
            parsing_result= parsing_result
        ).treat_results()

        # suppression du fichier
        os.unlink(path= file_path)

        return {
            "success": False,
            "error": "Erreur de test"
        }

        return {
            "success": True,
            "datas": {
                "textualDatas": {}
            }
        }
    except CustomException as e:
        if os != None:
            os.unlink(path= file_path)

        return {
            "success": False,
            "error": e.get_error_message()
        }
    except:
        if os != None:
            os.unlink(path= file_path)
            
        return {
            "success": False,
            "error": "Une erreur s'est produite sur le serveur"
        }

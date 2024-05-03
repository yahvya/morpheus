"""
    @brief Api morpheus
"""

import os
from fastapi import FastAPI, File, Header, UploadFile, Form
from api_utils.utils import CustomException, check_signature, temporary_upload
from detection.video_parser import VideoParser

app = FastAPI()

"""
    @brief Traitement de l'application mobile
"""
@app.post("/morpheus-mobile")
async def manage_mobile_app_request(
    signature: str = Header(...),
    video: UploadFile = File(...),
    mallampatiScore: int = Form(...),
):
    file_path = None

    try:
        # vérification de la signature
        check_signature(signature= signature)
        
        # création de la sauvegarde
        file_path = temporary_upload(file= video)

        VideoParser.parse(video_path= file_path)

        # suppression du fichier
        os.unlink(path= file_path)

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

"""
    @brief Api morpheus
"""

from fastapi import FastAPI, File, Header, UploadFile
from api_utils.utils import CustomException,check_signature

app = FastAPI()

"""
    @brief Traitement de l'application mobile
"""
@app.post("/morpheus-mobile")
async def manage_mobile_app_request(
    signature: str = Header(...),
    video: UploadFile = File(...)
):
    try:
        # vérification de la signature
        check_signature(signature= signature)

        return {
            "success": True,
            "datas": {}
        }
    except CustomException as e:
        return {
            "success": False,
            "error": e.get_error_message()
        }
    except:
        return {
            "success": False,
            "error": "Une erreur s'est produite sur le serveur"
        }

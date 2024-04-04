##
# @brief point d'entrée de l'api du projet Morpheus
# @author Vitalli https://github.com/siegward-from

from fastapi import FastAPI, UploadFile, File, Request, Form, Header

from api.utils import check_signature, save_upload_file, get_secret_key, generate_signature, save_files
from treatment.detection.detector import Detector, DetectorArg
from treatment.exceptions.custom_exception import CustomException
import os


app = FastAPI()


@app.post("/video")
async def treat_video(
        signature: str = Header(...),
        front_video: UploadFile = File(...),
        front_head_move_video: UploadFile = File(...),
        profile_head_up_video: UploadFile = File(...),
        profile_head_down_video: UploadFile = File()
):

    try:
        files = [front_video, front_head_move_video, profile_head_up_video, profile_head_down_video]
        video_paths = await save_files(files)
        check_signature(video_paths, signature)

        await Detector.extract_datas(DetectorArg(
            front_video,
            front_head_move_video,
            profile_head_up_video,
            profile_head_down_video
        ))

        return {
            "success": True,
            "result": {}
        }

    except CustomException as e:
        return {
            "success": False,
            "result": e.get_error_message()
        }

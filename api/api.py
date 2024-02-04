##
# @brief point d'entrée de l'api du projet Morpheus
# @author Vitalli https://github.com/siegward-from

from fastapi import FastAPI, UploadFile, File

from treatment.detection.detector import Detector, DetectorArg
from treatment.exceptions.custom_exception import CustomException

app = FastAPI()


@app.post("/video")
async def treat_video(
        front_video: UploadFile = File(...),
        front_head_move_video: UploadFile = File(...),
        profile_head_up_video: UploadFile = File(...),
        profile_head_down_video: UploadFile = File()
):
    try:
        await Detector.extract_datas(DetectorArg(
            front_video,
            front_head_move_video,
            profile_head_up_video,
            profile_head_down_video
        ))

        return "ok"
    except CustomException as e:
        return e.get_error_message()

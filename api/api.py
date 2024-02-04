##
# @brief point d'entrée de l'api du projet Morpheus
# @author Vitalli https://github.com/siegward-from

from fastapi import FastAPI, UploadFile, File

from treatment.detection.detector import DetectorArg

app = FastAPI()


@app.post("/test")
async def test(file: UploadFile = File(...)):
    return {"result": DetectorArg.are_videos(file)}
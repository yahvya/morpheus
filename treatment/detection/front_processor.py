##
# @brief module gérant la détection sur une vidéo de face
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from fastapi import UploadFile
import cv2
import mediapipe

from treatment.exceptions.custom_exception import CustomException


##
# @brief gestion de la détection de face
class FrontProcessor:
    @staticmethod
    def process(video: UploadFile):
        try:
            with mediapipe.solutions.face_mesh.FaceMesh() as extractor:
                video_manager = cv2.VideoCapture(video.file.name)

                while True:
                    # lecture de la frame
                    success, frame = video_manager.read()

                    if not success:
                        break

                    # récupération des détections
                    converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = extractor.process(converted_frame)

                    if results.multi_face_landmarks is None:
                        continue

                    landmarks = results.multi_face_landmarks[0]


                    print(landmarks)
        except Exception as e:
            print(e)
            raise CustomException("Une erreur s'est produite lors du traitement de la vidéo de face", True)

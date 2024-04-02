##
# @brief module gérant la détection sur une vidéo de face
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from fastapi import UploadFile
import cv2
import mediapipe
from math import sqrt,pow

from treatment.exceptions.custom_exception import CustomException


##
# @brief gestion de la détection de face
class FrontProcessor:
    ##
    # @brief index des landmarks de la bouche
    MOUTH_LANDMARKS_INDEXES = {"up" : 0, "down" : 17}
    
    ##
    # @brief Récupère 
    @staticmethod
    def process(video: UploadFile):
        try:
            with mediapipe.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                                        min_detection_confidence=0.5,
                                                        min_tracking_confidence=0.5) as extractor:
                video_manager = cv2.VideoCapture(video.file.name)

                max_distance = -1

                while True:
                    # lecture de la frame
                    success, frame = video_manager.read()

                    if not success:
                        break

                    # récupération de la distance sur la détection
                    success, distance = FrontProcessor.get_distance_between_detections(frame, extractor)

                    if not success:
                        continue

                    if distance > max_distance:
                        distance = max_distance

                # Release video capture
                video_manager.release()
                cv2.destroyAllWindows()
                
                if max_distance == -1:
                    raise CustomException("Aucune distance n'a pu être détectée", True)
                
                return {
                    "max_distance_between_open_mouth": max_distance
                }
        except CustomException as e:
            raise e
        except Exception as e:
            print(e)
            raise CustomException("Une erreur s'est produite lors du traitement de la vidéo de face", True)

    @staticmethod
    def get_distance_between_detections(frame: any, extractor: any) -> tuple[bool, float | None]:
        results = extractor.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) 

        if results.multi_face_landmarks:
            # récupération des détections du visage détecté
            landmarks = results.multi_face_landmarks[0]
        
            
            if FrontProcessor.MOUTH_LANDMARKS_INDEXES["up"] not in landmarks or FrontProcessor.MOUTH_LANDMARKS_INDEXES["down"] not in landmarks:
                return False, None
            
            # calcul de la distance
            image_h, image_w, _ = frame.shape
            
            mouth_up_landmark = landmarks.landmark[FrontProcessor.MOUTH_LANDMARKS_INDEXES["up"]]
            mouth_down_landmark = landmarks.landmark[FrontProcessor.MOUTH_LANDMARKS_INDEXES["down"]]
            
            # normalisation des coordonnées au format pixel
            mouth_up_x = int(mouth_up_landmark.x * image_w)
            mouth_up_y = int(mouth_up_landmark.y * image_h)
            
            mouth_down_x = int(mouth_down_landmark.x * image_w)
            mouth_down_y = int(mouth_down_landmark.y * image_h)
            
            return True, sqrt(pow(mouth_down_x - mouth_up_x,2) + pow(mouth_down_y - mouth_up_y,2) )
        
        return False, None

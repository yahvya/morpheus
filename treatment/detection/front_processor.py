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
                count = 0  # Counter for frames with detected face

                while True:
                    # lecture de la frame
                    success, frame = video_manager.read()


                    if not success:
                        break
                    
                    # test 
                    if count < 6:

                      landmark_indices = [0, 17]  # Example landmark indices
                      face_frame = FrontProcessor.crop_face(frame, extractor)
                      if face_frame is not None:
                         colored_face_frame = FrontProcessor.detect_and_color_landmarks_in_face(face_frame, extractor, landmark_indices, color=(0, 0, 255))
                         
                         if colored_face_frame is not None:
                          cv2.imshow("Colored Face Frame", colored_face_frame)
                          cv2.waitKey(0)
                          cv2.destroyAllWindows()
                         
                        #  cv2.imwrite(f"frame_{count}.jpg", colored_face_frame)
                      count += 1

                    
                    


                    # récupération de la distance sur la détection
                    success, distance = FrontProcessor.get_distance_between_detections(frame, extractor)
                    
                    # print(distance)
            
                    if distance is None:
                        continue

                    if distance > max_distance:
                        max_distance = distance
                        

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
            
        
            
            # if FrontProcessor.MOUTH_LANDMARKS_INDEXES["up"] not in landmarks or FrontProcessor.MOUTH_LANDMARKS_INDEXES["down"] not in landmarks:
            #     return False, None
            
            if not all(FrontProcessor.MOUTH_LANDMARKS_INDEXES[key] in landmarks.landmark for key in FrontProcessor.MOUTH_LANDMARKS_INDEXES):
                
            #   print("landmarks not found")
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
    
    # fc to  crop face
    @staticmethod
    def crop_face(frame: any, extractor: any, margin: int = 100) -> any:
     results = extractor.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

     if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]

        image_h, image_w, _ = frame.shape

        min_x, min_y = image_w, image_h
        max_x, max_y = 0, 0
        for landmark in landmarks.landmark:
            x = int(landmark.x * image_w)
            y = int(landmark.y * image_h)
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        # Add margin to the bounding box
        min_x = max(0, min_x - margin)
        min_y = max(0, min_y - margin)
        max_x = min(image_w, max_x + margin)
        max_y = min(image_h, max_y + margin)

        face_frame = frame[min_y:max_y, min_x:max_x]

        # Adjust landmark indices based on the new cropped frame
        for landmark in landmarks.landmark:
            landmark.x -= min_x / image_w
            landmark.y -= min_y / image_h

        return face_frame

     return None
    @staticmethod
    def detect_and_color_landmarks_in_face(face_frame: any, face_extractor: any, landmark_indices: list, color: tuple = (0, 255, 0)) -> any:
    # Convert the face frame to RGB format
     rgb_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)

    # Detect landmarks in the face frame
     results = face_extractor.process(rgb_frame)

     if results.multi_face_landmarks:
        # Get landmarks of the first detected face
        landmarks = results.multi_face_landmarks[0]

        # Convert landmarks to pixel coordinates
        image_h, image_w, _ = face_frame.shape
        pixel_landmarks = []
        for index in landmark_indices:
            if 0 <= index < len(landmarks.landmark):
                x = int(landmarks.landmark[index].x * image_w)
                y = int(landmarks.landmark[index].y * image_h)
                pixel_landmarks.append((x, y))
                # Draw a circle around the landmark point
                cv2.circle(face_frame, (x, y), 3, color, -1)  # -1 means filled circle

      

        return face_frame

     return None



from typing import Any, List

import cv2
import numpy
import os
from detection.utils.important_landmarks import MarkerImportLandmarks
from numpy import dtype, generic, ndarray
from mediapipe import solutions
from detection.utils.utils import new_face_detector

classifiers_path = f"{os.path.dirname(__file__)}/resources/haarcascades/"
  
"""
    @brief Détecteurs
"""
pose_detector = solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.8)
face_detector = new_face_detector()
left_ear_cascade = cv2.CascadeClassifier(f"{classifiers_path}leftear.xml")
right_ear_cascade = cv2.CascadeClassifier(f"{classifiers_path}rightear.xml")

"""
    @brief Fonction de détection customisé du marqueur du cou
    @param frame La frame à traiter
    @param important_landmarks liste des landmarks important à détecter
    @return map des détections faîtes
"""
def detect_neck_marker(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    important_landmarks: List[int]
) -> dict[int,dict[str,int]]:
    try:
        """
            Récupération de la zone du cou dans l'image par coupure entre l'épaule droite et l'oreille droite
        """
        converted_frame = cv2.cvtColor(src= frame, code= cv2.COLOR_BGR2RGB)
        detected_poses = pose_detector.process(converted_frame)

        if not detected_poses.pose_landmarks:
            return {}
        
        pose_landmarks = detected_poses.pose_landmarks.landmark
        expected_landmarks = [
            solutions.pose.PoseLandmark.RIGHT_SHOULDER.value,
            solutions.pose.PoseLandmark.NOSE.value
        ]

        """
            Vérification de présence des landmarks ainsi que de l'oreille droite dans le champ et récupération des coordonnées de zone
        """

        if len(pose_landmarks) - 1 < max(expected_landmarks):
            return {}

        left_shoulder_landmark = pose_landmarks[solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
        nose_landmark = pose_landmarks[solutions.pose.PoseLandmark.NOSE.value]

        if None in [left_shoulder_landmark, nose_landmark] or len(detect_right_profile_marker(frame= frame, important_landmarks= important_landmarks)) == 0:
            return {}

        image_height, _, __ = converted_frame.shape
        image_height = int(image_height)
        start_y = nose_landmark.y * image_height
        end_y = left_shoulder_landmark.y * image_height

        """
            Récupération des marqueurs et récupération de celui qui se trouve dans la zone du coup
        """
        founded_markers = find_circles_in_frame(
            frame= frame,
            hsv_lower = [89, 0, 0],
            hsv_upper = [125, 255, 255],
            min_radius= 6,
            max_radius= 25
        )

        for marker_data in founded_markers:
            (marker_center_x, marker_center_y), radius = marker_data

            if not (marker_center_y > start_y and marker_center_y < end_y ):
                continue

            return {
                MarkerImportLandmarks.ADAM_APPLE.value: {
                    "x": marker_center_x,
                    "y": marker_center_y,
                    "radius": radius
                }
            }

        return {}
    except:
        return {}

"""
    @brief Fonction de détection customisé du marqueur de référence de face
    @param frame La frame à traiter
    @param important_landmarks liste des landmarks important à détecter
    @return map des détections faîtes
"""
def detect_front_reference_marker(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    important_landmarks: List[int]
):
    try:
        """
            Récupération de la zone du front par séparation entre le haut de la tête et le nez
        """
        converted_frame = cv2.cvtColor(src= frame, code= cv2.COLOR_BGR2RGB)
        founded_faces = face_detector.process(converted_frame)

        if not founded_faces.multi_face_landmarks:
            return {}
        
        founded_landmarks = founded_faces.multi_face_landmarks[0].landmark
        top_limiter_index = 10
        bottom_limiter_index = 8
        left_limiter_index = 66
        right_limiter_index = 296

        if (
            len(founded_landmarks) <= max([
                top_limiter_index,
                bottom_limiter_index,
                left_limiter_index,
                right_limiter_index
            ]) or 
            None in [
                founded_landmarks[top_limiter_index],
                founded_landmarks[bottom_limiter_index],
                founded_landmarks[left_limiter_index],
                founded_landmarks[right_limiter_index]
            ]
        ):
            return {}

        image_height, image_width, __ = converted_frame.shape
        top_landmark_y = int(founded_landmarks[top_limiter_index].y * image_height)
        bottom_landmark_y = int(founded_landmarks[bottom_limiter_index].y * image_height)
        left_limiter_x = int(founded_landmarks[left_limiter_index].x * image_width)
        right_limiter_x = int(founded_landmarks[right_limiter_index].x * image_width)

        """
           Recherche des marqueurs dans la zone fournie 
        """
        founded_markers = find_circles_in_frame(
            frame= frame,
            hsv_lower = [89, 0, 0],
            hsv_upper = [125, 255, 255],
            min_radius= 6,
            max_radius= 25
        )

        for marker_data in founded_markers:
            (marker_center_x, marker_center_y), radius = marker_data

            if not (marker_center_y >= top_landmark_y and marker_center_y <= bottom_landmark_y and marker_center_x >= left_limiter_x and marker_center_x <= right_limiter_x):
                continue

            return {
                MarkerImportLandmarks.FRONT_REFERENCE.value : {
                    "x": marker_center_x,
                    "y": marker_center_y,
                    "radius": radius
                }
            }

        return {}
    except:
        return {}

"""
    @brief Fonction de détection customisé du marqueur de référence du profile gauche
    @param frame La frame à traiter
    @param important_landmarks liste des landmarks important à détecter
    @return map des détections faîtes
"""
def detect_left_profile_marker(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    important_landmarks: List[int]
):
    try:
        if left_ear_cascade.empty() or right_ear_cascade.empty():
            return {}

        """
            Vérifie que la personne soit de profil gauche en vérifiant la présence d'une oreille gauche et pas d'oreille droite sur la frame
        """
        converted_frame = cv2.cvtColor(src= frame, code= cv2.COLOR_BGR2GRAY)
        left_ears = left_ear_cascade.detectMultiScale(image= converted_frame,scaleFactor= 1.3, minNeighbors= 0) 
        right_ears = right_ear_cascade.detectMultiScale(image= converted_frame,scaleFactor= 1.3, minNeighbors= 0) 
        
        if len(left_ears) != 1 or len(right_ears) > 0:
            return {}

        (_, y, __, height) = left_ears[0]
        margin = 40
        start_y = max(y - margin, 0)
        end_y = min(y + height + margin,converted_frame.shape[0]) 

        """
            Récupération et extraction des marqueurs        
        """

        founded_markers = find_circles_in_frame(
            frame= frame,
            hsv_lower = [89, 0, 0],
            hsv_upper = [125, 255, 255],
            min_radius= 6,
            max_radius= 25
        )

        for marker_data in founded_markers:
            (marker_center_x, marker_center_y), radius = marker_data

            if marker_center_y > start_y and marker_center_y < end_y:
                return {
                    MarkerImportLandmarks.LEFT_PROFILE_REFERENCE.value : {
                        "x": marker_center_x,
                        "y": marker_center_y,
                        "radius": radius
                    }
                }

        return {}
    except:
        return {}

"""
    @brief Fonction de détection customisé du marqueur de référence du profil droit
    @param frame La frame à traiter
    @param important_landmarks liste des landmarks important à détecter
    @return map des détections faîtes
"""
def detect_right_profile_marker(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    important_landmarks: List[int]
):
    try:
        if left_ear_cascade.empty() or right_ear_cascade.empty():
            return {}

        """
            Vérifie que la personne soit de profil droit en vérifiant la présence d'une oreille droite et pas d'oreille gauche sur la frame
        """
        converted_frame = cv2.cvtColor(src= frame, code= cv2.COLOR_BGR2GRAY)
        left_ears = left_ear_cascade.detectMultiScale(image= converted_frame,scaleFactor= 1.3, minNeighbors= 0) 
        right_ears = right_ear_cascade.detectMultiScale(image= converted_frame,scaleFactor= 1.3, minNeighbors= 0) 
        
        if len(right_ears) != 1 or len(left_ears) > 0:
            return {}

        (_, y, __, height) = right_ears[0]
        margin = 40
        start_y = max(y - margin, 0)
        end_y = min(y + height + margin,converted_frame.shape[0]) 

        """
            Récupération et extraction des marqueurs        
        """

        founded_markers = find_circles_in_frame(
            frame= frame,
            hsv_lower = [89, 0, 0],
            hsv_upper = [125, 255, 255],
            min_radius= 6,
            max_radius= 25
        )

        for marker_data in founded_markers:
            (marker_center_x, marker_center_y), radius = marker_data

            if marker_center_y > start_y and marker_center_y < end_y:
                return {
                    MarkerImportLandmarks.RIGHT_PROFILE_REFERENCE.value : {
                        "x": marker_center_x,
                        "y": marker_center_y,
                        "radius": radius
                    }
                }

        return {}
    except:
        return {}

"""
    @brief Recherche les cercles dans la frame fournie
    @param frame la frame
    @param min_radius rayon minimum de recherche
    @param max_radius rayon maximum de recherche
    @param hsv_lower range de couleur minimum
    @param hsv_upper range de couleur maximum
    @return liste des centres (x,y) des cercles
"""
def find_circles_in_frame(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    hsv_lower: List[int],
    hsv_upper: List[int],
    min_radius:int = 3,
    max_radius:int = 7
):
    circles = []

    try:
        hsv = cv2.cvtColor(src= frame,code= cv2.COLOR_BGR2HSV)

        lower_pink = numpy.array(object= hsv_lower)
        upper_pink = numpy.array(object= hsv_upper)

        mask = cv2.inRange(src= hsv, lowerb= lower_pink,upperb= upper_pink)
        contours, _ = cv2.findContours(image= mask,mode= cv2.RETR_TREE,method= cv2.CHAIN_APPROX_SIMPLE) 

        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(points= contour)
            center = (int(x), int(y))
            radius = int(radius)

            if radius >= min_radius and radius <= max_radius:
                circles.append((center, radius))
    except:
        pass

    return circles

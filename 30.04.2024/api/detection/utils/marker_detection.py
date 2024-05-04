from typing import Any, List

import cv2
import numpy
from detection.utils.important_landmarks import MarkerImportLandmarks
from numpy import dtype, generic, ndarray
from mediapipe import solutions
from detection.utils.utils import new_face_detector

"""
    @brief Détecteur de pose
"""
pose_detector = solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
face_detector = new_face_detector()

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
            Récupération de la zone du cou dans l'image par coupure entre les épaules et le nez
        """
        converted_frame = cv2.cvtColor(src= frame, code= cv2.COLOR_BGR2RGB)
        detected_poses = pose_detector.process(converted_frame)

        if not detected_poses.pose_landmarks:
            return {}
        
        pose_landmarks = detected_poses.pose_landmarks.landmark
        expected_landmarks = [
            solutions.pose.PoseLandmark.LEFT_SHOULDER.value,
            solutions.pose.PoseLandmark.NOSE.value
        ]

        """
            Vérification de présence des landmarks et récupération des coordonnées de zone
        """

        if len(pose_landmarks) - 1 < max(expected_landmarks):
            return {}

        left_shoulder_landmark = pose_landmarks[solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
        nose_landmark = pose_landmarks[solutions.pose.PoseLandmark.NOSE.value]

        if None in [left_shoulder_landmark, nose_landmark]:
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
            hsv_lower= [0, 0, 0],    
            hsv_upper= [170, 255, 255],
            min_radius= 3,
            max_radius=20  
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
        head_top_landmark_index = 10
        nose_landmark_index = 195

        if len(founded_landmarks) <= 195:
            return {}

        image_height, image_width, _ = converted_frame.shape
        head_top_landmark_y = int(founded_landmarks[head_top_landmark_index].y * image_height)
        nose_landmark_y = int(founded_landmarks[nose_landmark_index].y * image_height)

        """
           Recherche des marqueurs dans la zone fournie 
        """
        founded_markers = find_circles_in_frame(
            frame= frame,
            hsv_lower= [0, 0, 0],    
            hsv_upper= [170, 255, 255],
            min_radius= 5,
            max_radius= 15  
        )

        for marker_data in founded_markers:
            (marker_center_x, marker_center_y), radius = marker_data

            if not (marker_center_y > head_top_landmark_y and marker_center_y < nose_landmark_y):
                continue

            return {
                MarkerImportLandmarks.FRONT_REFERENCE.value : {
                    "x": marker_center_x,
                    "y": marker_center_y,
                    "radius": radius
                }
            }

        return {}
    except Exception as e:
        print(e)
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
    max_radius:int = 20
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
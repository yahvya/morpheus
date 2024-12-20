import cv2
import numpy
import os
from typing import Any, List
from detection.utils.important_landmarks import MarkerImportLandmarks, ImportantLandmarks
from numpy import dtype, generic, ndarray
from detection.utils.utils import new_face_detector

"""
    @brief Détecteurs
"""
face_detector = new_face_detector()

"""
    @brief Fonction de détection customisé du marqueur du cou
    @param frame La frame à traiter
    @param important_landmarks liste des landmarks important à détecter
    @param important_landmarks_datas_in_frame liste des détections faîtes sur les landmarks important
    @return map des détections faîtes
"""
def detect_neck_marker(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    important_landmarks: List[int],
    important_landmarks_datas_in_frame: dict[int,dict[str,int|float]]
) -> dict[int,dict[str,int]]:
    try:  
        # cv2.namedWindow("test",cv2.WINDOW_GUI_NORMAL)
        # cv2.resizeWindow("test",400,400)
        # cv2.imshow("test",frame)
        # cv2.waitKey(5)
        # print("debut")
        # print(pose_landmarks[left_shoulder_index])
        # print(pose_landmarks[right_shoulder_index])
        # print("fin")

        # image_height, image_width, __ = converted_frame.shape
        # top_landmark_y = int(founded_landmarks[top_limiter_index].y * image_height)
        # bottom_landmark_y = int(founded_landmarks[bottom_limiter_index].y * image_height)
        # left_limiter_x = int(founded_landmarks[left_limiter_index].x * image_width)
        # right_limiter_x = int(founded_landmarks[right_limiter_index].x * image_width)

        # """
        #     Coupure et redimensionnement de la frame sur la zone attendue
        # """
        # sub_frame = cv2.resize(frame[top_landmark_y:bottom_landmark_y, left_limiter_x:right_limiter_x],(200,200))

        # """
        #    Recherche des marqueurs dans la zone fournie 
        # """
        # founded_markers = find_circles_in_frame(
        #     frame= sub_frame,
        #     hsv_lower = [89, 0, 0],
        #     hsv_upper = [125, 255, 255],
        #     min_radius= 20,
        #     max_radius= 24
        # )

        # """
        #     Calcul des facteurs de redimensionnement    
        # """
        # base_width = right_limiter_x - left_limiter_x
        # base_height = bottom_landmark_y - top_landmark_y
        # width_resize_factor = 200 / base_width
        # height_resize_factor = 200 / base_height

        # for marker_data in founded_markers:
        #     (marker_center_x, marker_center_y), radius = marker_data

        #     """
        #         Replacement des valeurs redimensionnées
        #     """
        #     marker_center_x = int((marker_center_x / width_resize_factor))
        #     marker_center_y = int(marker_center_y / height_resize_factor)
        #     radius = int(radius / max(width_resize_factor,height_resize_factor))

        #     """
        #         Décalage à partir de sous image
        #     """
        #     marker_center_x += left_limiter_x
        #     marker_center_y += top_landmark_y

        #     return {
        #         MarkerImportLandmarks.ADAM_APPLE.value : {
        #             "x": marker_center_x,
        #             "y": marker_center_y,
        #             "radius": radius
        #         }
        #     }

        return {}
    except Exception as e:
        print(e)
        return {}

"""
    @brief Fonction de détection customisé du marqueur de référence de face
    @param frame La frame à traiter
    @param important_landmarks liste des landmarks important à détecter
    @param important_landmarks_datas_in_frame liste des détections faîtes sur les landmarks important
    @return map des détections faîtes
"""
def detect_front_reference_marker(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    important_landmarks: List[int],
    important_landmarks_datas_in_frame: dict[int,dict[str,int|float]]
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
            Coupure et redimensionnement de la frame sur la zone attendue
        """
        sub_frame = cv2.resize(src= frame[top_landmark_y:bottom_landmark_y, left_limiter_x:right_limiter_x],dsize= (200,200))

        """
           Recherche des marqueurs dans la zone fournie 
        """
        founded_markers = find_circles_in_frame(
            frame= sub_frame,
            hsv_lower = [89, 0, 0],
            hsv_upper = [125, 255, 255],
            min_radius= 20,
            max_radius= 24
        )

        """
            Calcul des facteurs de redimensionnement    
        """
        base_width = right_limiter_x - left_limiter_x
        base_height = bottom_landmark_y - top_landmark_y
        width_resize_factor = 200 / base_width
        height_resize_factor = 200 / base_height

        for marker_data in founded_markers:
            (marker_center_x, marker_center_y), radius = marker_data

            """
                Replacement des valeurs redimensionnées
            """
            marker_center_x = int((marker_center_x / width_resize_factor))
            marker_center_y = int(marker_center_y / height_resize_factor)
            radius = int(radius / max(width_resize_factor,height_resize_factor))

            """
                Décalage à partir de sous image
            """
            marker_center_x += left_limiter_x
            marker_center_y += top_landmark_y

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
    min_radius:int,
    max_radius:int
):
    circles = []

    try:
        hsv = cv2.cvtColor(src= frame,code= cv2.COLOR_BGR2HSV)

        lower_bound = numpy.array(object= hsv_lower)
        upper_bound = numpy.array(object= hsv_upper)

        mask = cv2.inRange(src= hsv, lowerb= lower_bound,upperb= upper_bound)
        contours, _ = cv2.findContours(image= mask,mode= cv2.RETR_TREE,method= cv2.CHAIN_APPROX_SIMPLE) 

        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(points= contour)
            center = (int(x), int(y))
            radius = int(radius)

            if radius >= min_radius and radius <= max_radius:
                circles.append((center, radius))
                # cv2.circle(frame,(int(x),int(y)),radius,[255,255,0])
                # cv2.putText(
                #     img= frame,
                #     text= f"{radius}",
                #     org= (int(x + 10),int(y)),
                #     fontFace= cv2.FONT_HERSHEY_COMPLEX,
                #     fontScale= 1,
                #     color= [255,255,0]
                # )
                # cv2.imshow("test",frame)
                # cv2.waitKey()
    except:
        pass
    
    return circles

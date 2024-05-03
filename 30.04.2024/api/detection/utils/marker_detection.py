from typing import Any, List

import cv2
from numpy import dtype, generic, ndarray
import numpy

"""
    @brief Fonction de détection customisé (marqueurs)
    @param frame La frame à traiter
    @param important_landmarks liste des landmarks important à détecter
    @return map des détections faîtes
"""
def detect_marker(
    frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
    important_landmarks: List[int]
) -> dict[int,dict[str,int]]:
    """
        Récupération des marqueurs et recherche de celui placé au niveau du cou
    """
    founded_markers = find_circles_in_frame(
        frame= frame,
        hsv_lower= [0, 0, 0],    
        hsv_upper= [170, 255, 255]   
    )



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
        contours, _ = cv2.findContours(src= mask,mode= cv2.RETR_TREE,method= cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(points= contour)
            center = (int(x), int(y))
            radius = int(radius)

            if radius >= min_radius and radius <= max_radius:
                circles.append((center, radius))
    except:
        pass

    return circles
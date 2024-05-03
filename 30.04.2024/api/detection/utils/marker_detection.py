from typing import Any, List

import cv2
from numpy import dtype, generic, ndarray

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
    return {}
import cv2
import time
import os
from math import pow, sqrt
from typing import Any, Tuple
from numpy import dtype, generic, ndarray

"""
    @brief Traiteur des informations vidéos
"""
class Treatment:
    """
        @brief Dessine le point sur la frame fournie
        @param drawable_frame frame de dessin
        @param landmark données du point à dessiner
        @param drawing_color couleur du dessin
    """
    @staticmethod
    def draw_landmark_on(
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
        landmark: dict[str,any],
        drawing_color: Tuple[int, int, int]
    ):
        cv2.circle(
            img= drawable_frame,
            center= (landmark["datas"]["x"], landmark["datas"]["y"]),
            radius= landmark["datas"]["radius"] if "radius" in landmark["datas"] else 5,
            color= drawing_color,
            thickness= -1
        )

    """
        @brief Dessine le point sur la frame fournie
        @param drawable_frame frame de dessin
        @param landmark_one données du premier point à dessiner
        @param landmark_two données du second point à dessiner
        @param drawing_color couleur du dessin
    """
    @staticmethod
    def draw_line_between(
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
        landmark_one: dict[str,any],
        landmark_two: dict[str,any],
        drawing_color: Tuple[int, int, int]
    ):
        cv2.line(
            img= drawable_frame,
            pt1= (landmark_one["datas"]["x"], landmark_one["datas"]["y"]),
            pt2= (landmark_two["datas"]["x"], landmark_two["datas"]["y"]),
            color= drawing_color,
            thickness= 4
        )

    """
        @brief Dessine le texte à côté du point fourni
        @param drawable_frame frame de dessin
        @param landmark landmark à côté duquel dessiner
        @param text message
        @param drawing_color couleur de dessin
    """
    @staticmethod
    def draw_text_near(
        drawable_frame: cv2.Mat | ndarray[Any, dtype[generic]] | ndarray,
        landmark: dict[str,any],
        text: str,
        drawing_color: Tuple[int, int, int]
    ):
        cv2.putText(
            img= drawable_frame,
            text= text,
            org= (landmark["datas"]["x"],landmark["datas"]["y"]),
            fontFace= cv2.FONT_HERSHEY_COMPLEX,
            fontScale= 3,
            color= drawing_color
        )

    """
        @brief Calcul l'équavlence entre pixel et centimètre
        @param reference_landmark données du référenciel
        @param real_value valeur attendue
        @return la valeur de référence
    """
    @staticmethod
    def get_a_pixel_value_in_centimer(reference_landmark: dict[str,int|float], real_value:int) -> int|float:
        return reference_landmark["datas"]["radius"] / real_value

    """
        @brief Calcule la distance en pixel entre les deux points fournis
        @param landmark_one point 1
        @param landmark_two point 2
        @return La distance en pixel
    """
    @staticmethod
    def calculate_pixel_distance_between(landmark_one: dict[str,any],landmark_two: dict[str,any]) -> int |float:
        landmark_one_coords = landmark_one["datas"]
        landmark_two_coords = landmark_two["datas"]

        return sqrt(
            pow(landmark_one_coords["x"] - landmark_two_coords["x"],2) +
            pow(landmark_one_coords["y"] - landmark_two_coords["y"],2)
        )

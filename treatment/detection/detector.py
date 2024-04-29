##
# @brief module gérant la détection
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub
from math import sqrt
from typing import Any

from treatment.detection.detector_result import DetectorResult
from treatment.exceptions.custom_exception import CustomException
from starlette.datastructures import UploadFile
import filetype


##
# @brief données nécessaires à l'extraction des points
class DetectorArg:
    ##
    # @brief vidéo de face de la personne puis ouvre la bouche (UploadFile)
    __front_video: UploadFile

    ##
    # @brief vidéo de face de la personne puis lève la tête (UploadFile)
    __front_head_move_video: UploadFile

    ##
    # @brief vidéo de profil de la personne puis baisse la tête (UploadFile)
    __profile_head_down_video: UploadFile

    ##
    # @brief vidéo de profil de la personne puis lève la tête (UploadFile)
    __profile_head_up_video: UploadFile

    ##
    # @param front_video vidéo de face de la personne puis ouvre la bouche (UploadFile)
    # @param front_head_move_video vidéo de face de la personne et lève la tête (UploadFile)
    # @param profile_head_down_video vidéo de profil de la personne et baisse la tête (UploadFile)
    # @param profile_head_up_video vidéo de profil de la personne et lève la tête (UploadFile)
    # @throws CustomException en cas d'erreur
    def __init__(
            self,
            front_video: UploadFile,
            front_head_move_video: UploadFile,
            profile_head_down_video: UploadFile,
            profile_head_up_video: UploadFile
    ):
        # vérification du format des vidéos

        if not DetectorArg.are_videos(
                front_video,
                front_head_move_video,
                profile_head_down_video,
                profile_head_up_video
        ):
            raise CustomException("Format inconnu de fichier", True)

        self.__front_video = front_video
        self.__profile_head_up_video = profile_head_up_video
        self.__front_head_move_video = front_head_move_video
        self.__profile_head_down_video = profile_head_down_video

    ##
    # @return vidéo de face de la personne puis ouvre la bouche (UploadFile)
    def get_front_video(self) -> UploadFile:
        return self.__front_video

    ##
    # @return vidéo de face de la personne puis lève la tête (UploadFile)
    def get_front_head_move_video(self) -> UploadFile:
        return self.__front_head_move_video

    ##
    # @return vidéo de profil de la personne puis baisse la tête (UploadFile)
    def get_profile_head_down_video(self) -> UploadFile:
        return self.__profile_head_down_video

    ##
    # @return vidéo de profil de la personne puis lève la tête (UploadFile)
    def get_profile_head_up_video(self) -> UploadFile:
        return self.__profile_head_up_video

    ##
    # @brief vérifie que les paramètres fournis sont bien des vidéos
    # @param *videos liste des fichiers à vérifier (UploadFile)
    # @return si tous les élements envoyés sont valides
    @staticmethod
    def are_videos(*videos: UploadFile) -> bool:
        return (
                len(videos) != 0 and
                all(
                    isinstance(potential_video, UploadFile) and
                    filetype.is_video(potential_video.file)

                    for potential_video in videos
                )
        )


##
# @brief gestionnaire de détection de points
class Detector:
    ##
    # @brief extrait toutes les données à détecter
    # @param detection_datas donnée de détection (DectectorArg)
    # @return DetectorResult le résultat des détections faîtes
    # @throws CustomException en cas d'erreur
    @staticmethod
    async def extract_datas(detection_datas: DetectorArg) -> DetectorResult:
        from treatment.detection.front_processor import FrontProcessor

        try:
            ##
            # @todo finir le test et placer les résultats dans le detectorresul
            FrontProcessor.process(detection_datas.get_front_video())

            return DetectorResult()
        except CustomException as e:
            raise e
        except Exception as _:
            raise CustomException("Une erreur s'est produite lors du traitement des données", True)

    ##
    # @brief Fourni la valeur associée à un centimètre en fonction des valeurs
    # @param landmarks les landmarks à traiter
    # @param references_landmarks_indexes index des landmarks de références
    # @param frame_dimensions dimensions de la frame traitée
    # @param reference_value valeur de référence choisie
    # @return la valeur au format (success, valeur)
    @staticmethod
    def get_pixel_reference_value(landmarks: Any, references_landmarks_indexes: (int, int), frame_dimensions: (int, ...), reference_value: float):
        try:
            first_landmark, second_landmark = references_landmarks_indexes

            # vérification de présence de landmark
            if not max(first_landmark, second_landmark) < len(landmarks):
                return False, -1

            # récupération des valeurs
            first_landmark_value = landmarks[first_landmark]
            second_landmark_value = landmarks[second_landmark]

            distance_in_pixels = Detector.get_distance_between_landmarks_in_pixel(first_landmark_value, second_landmark_value, frame_dimensions)

            return True, distance_in_pixels / reference_value
        except Exception:
            return False, -1

    ##
    # @brief Fourni la distance en pixel entre deux landmarks dans une frame donnée
    @staticmethod
    def get_distance_between_landmarks_in_pixel(first_landmark, second_landmark, frame_dimensions: (int, ...)):
        # récupération des emplacements des points
        image_h, image_w,image_c = frame_dimensions

        up_x = int(first_landmark.x * image_w)
        up_y = int(first_landmark.y * image_h)
        up_z = int(first_landmark.z * image_c)
        down_x = int(second_landmark.x * image_w)
        down_y = int(second_landmark.y * image_h)
        down_z = int(second_landmark.z * image_c)

        return sqrt(((down_x - up_x) ** 2) + ((down_y - up_y) ** 2) + ((down_z - up_z) ** 2))

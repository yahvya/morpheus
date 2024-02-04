##
# @brief module gérant la détection
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from treatment.detection.detector_result import DetectorResult
from treatment.exceptions.custom_exception import CustomException
from starlette.datastructures import UploadFile
import filetype


##
# @brief données nécessaires à l'extraction des points
class DetectorArg:
    ##
    # @brief front_video vidéo de face de la personne puis ouvre la bouche (UploadFile)
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
        pass

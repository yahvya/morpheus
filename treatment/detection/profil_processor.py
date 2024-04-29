##
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from enum import Enum

from fastapi import UploadFile

##
# @brief Définition du type de profile
class ProfileSide(Enum):
    ##
    # @brief Profil gauche
    LEFT = 1
    ##
    # @brief Profil droit
    RIGHT = 2

##
# @brief Gestionnaire de détection des points des vidéos de profil
class ProfileProcessor:
    @staticmethod
    def process(video: UploadFile,side: ProfileSide):
        pass
##
# @brief gestionnaire de détection du projet morpheus
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from enum import Enum
from custom_exception import CustomException
import json
import mediapipe as mp


##
# @brief représente les gestionnaires des données à extraire
# @todo compléter l'énumération avec les vraies valeurs
class ExtractManager(Enum):
    ##
    # les points de la bouche
    MOUTH = lambda video: True


##
# @brief gestion de la détection
class Detector:
    ##
    # @param config_file_path chemin du fichier de configuration
    # @throws CustomException en cas d'erreur
    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config:
                self.config = json.load(config)
        except Exception as _:
            raise CustomException("Echec de chargement du fichier de configuration", False)

    ##
    # @brief extrait les points demandé d'une vidéo
    # @param extract_managers gestionnaires des données à extraire. Liste de ExtractManager
    # @throws CustomException en cas d'erreur
    def extract_points_from(self, video, extract_managers):
        extract_results = []

        try:
            for manager in extract_managers:
                extract_managers.append(manager(video))
        except Exception as _:
            raise CustomException("Echec d'extraction des données", False)

        return extract_results

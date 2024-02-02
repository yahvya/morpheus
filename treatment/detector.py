##
# @brief gestionnaire de détection du projet morpheus
# @author https://github.com/yahvya/
# @author https://github.com/ChakerYaakoub

from custom_exception import CustomException
import json
import mediapipe as mp


##
# @brief gestion de la détection
class Detector:
    ##
    # @param config_file_path chemin du fichier de configuration
    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config:
                self.config = json.load(config)
        except Exception as _:
            raise CustomException("Echec de chargement du fichier de configuration", False)

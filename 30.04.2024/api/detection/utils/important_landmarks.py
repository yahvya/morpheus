from enum import Enum

"""
    @brief Landmarks important à récupérer
"""
class ImportantLandmarks(Enum):
    """
        @brief Pointe du menton
    """
    CHIN_CENTER = 175

    """
        @brief Mâchoire droite
    """
    RIGHT_JAW = 215

    """
        @brief Mâchoire gauche
    """
    LEFT_JAW = 435

    """
        @brief Lèvre supérieur
    """
    UPPER_LIP = 0

    """
        @brief Lèvre inférieur
    """
    LOWER_LIP = 17

"""
    @brief Landmarks customisés sur les marqueurs
"""
class MarkerImportLandmarks(Enum):
    """
        @brief Pomme d'adam
    """
    ADAM_APPLE = -1

    """
        @brief Marqueur de référence de face
    """
    FRONT_REFERENCE = -2

    """
        @brief Marqueur de référence du profil gauche
    """
    LEFT_PROFILE_REFERENCE = -3

    """
        @brief Marqueur de référence du profil droit
    """
    RIGHT_PROFILE_REFERENCE = -4
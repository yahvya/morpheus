from enum import Enum

"""
    @brief Landmarks important à récupérer
"""
class ImportantLandmarks(Enum):
    """
        @brief Oeil gauche
    """
    LEFT_EYE = 144

    """
        @brief Oeil droit
    """
    RIGHT_EYE = 373

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
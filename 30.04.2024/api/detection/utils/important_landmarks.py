from enum import Enum

"""
    @brief Landmarks important à récupérer
"""
class ImportantLandmarks(Enum):
    """
        @brief Pointe du menton
    """
    CHIN_CENTER = 152

    """
        @brief Pointe du menton décalé à droite
    """
    CHIN_RIGHT_CENTER = 148

    """
        @brief Mâchoire droite
    """
    RIGHT_JAW = 215

    """
        @brief Mâchoire gauche
    """
    LEFT_JAW = 435

    """
        @brief Tragus droit
    """
    RIGHT_TRAGUS = 234

    """
        @brief Tragus gauche
    """
    LEFT_TRAGUS = 454

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

"""
    @brief Résultat de traitement
"""
class TreatmentResult:
    """
        @brief Stock la distance maximum d'ouverture de bouche
        @param max_mouth_distance distance maximum d'ouverture de bouche
        @return self
    """
    def set_max_mouth_distance(self, max_mouth_distance: int|float) -> object:
        self.max_mouth_distance = max_mouth_distance
        return self

    """
        @return La distance maximum d'ouverture de bouche ou None si non affecté
    """
    def get_max_mouth_distance(self) -> int|float|None:
        return self.max_mouth_distance

    """
        @brief Stock le chemin de la vidéo récapitulative
        @param recap_video_path le chemin de la vidéo récapitulative
        @return self
    """
    def set_recap_video_path(self, recap_video_path: str) -> object:
        self.recap_video_path = recap_video_path
        return self
    
    """
        @return Le chemin de la vidéo récapitulative ou None si non affecté
    """
    def get_recap_video_path(self) -> str|None:
        return self.recap_video_path
    
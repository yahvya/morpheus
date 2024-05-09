from detection.video.parser_result import ParserResult

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
    
    """
        @brief Stock le résultat de parsing
        @param parse_result résultat de parsing
        @return self
    """
    def set_parse_result(self,parse_result: ParserResult) -> object:
        self.parse_result = parse_result
        return self
    
    """
        @return Le résultat de parsing ou None si non affecté
    """
    def get_parse_result(self) -> ParserResult|None:
        return self.parse_result
        
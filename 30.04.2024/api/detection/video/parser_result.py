"""
    @brief Résultat de parsing vidéo
"""
from typing import List


class ParserResult:
    def __init__(self) -> None:
        self.results = {}

    """
        @brief Sauvegarde les données du point
        @param frame_counter numéro de la frame dont provienne les données
        @param landmark index du point
        @param datas données du point
    """
    def add_frame_data(
        self,
        frame_counter:int,
        landmark:int,
        datas: any
    ):
        if not landmark in self.results:
            self.results[landmark] = []

        self.results[landmark].append({
            "frame-counter": frame_counter,
            "datas": datas 
        })

    """
        @brief Fourni l'entiereté des enregistrements du point fourni
        @param landmark le point
        @return Les enregistrements sur le point ou None si non trouvé
    """
    def get_landmark_datas(self, landmark: int) -> None|List[dict[str,any]]:
        return self.results[landmark] if landmark in self.results else None
    
    """
        @brief Fourni l'enregistrement sur le point à la frame fournie
        @param landmark le point
        @param frame_counter index de la frame
        @return L'enregistrement sur le point ou None si non trouvé
    """
    def get_landmark_datas_for_frame(self, landmark: int, frame_counter:int) -> None|dict[str,any]:
        if not landmark in self.results:
            return None

        for data in self.results[landmark]:
            if data["frame-counter"] == frame_counter:
                return data

        return None

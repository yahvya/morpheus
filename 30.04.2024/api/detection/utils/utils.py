from mediapipe import solutions

"""
    @brief Crée un nouveau détecteur de face
    @param max_num_faces nombre de visages max 
    @param redefine_landmarks formatage des coordonnées de points 
    @param min_detection_confidence fiabilité minimum de détection
    @param min_tracking_confidence fiabilité minimum du suivi de points
    @param static_image_mode défini s'il agit en mode stream vidéo (False) ou image statique (True)
    @doc https://mediapipe.readthedocs.io/en/latest/solutions/face_mesh.html
"""
@staticmethod
def new_face_detector(
    max_num_faces:int = 1, 
    redefine_landmarks = True,
    min_detection_confidence= 0.8,
    min_tracking_confidence=0.8,
    static_image_mode= False
) -> solutions.face_mesh.FaceMesh:
    return solutions.face_mesh.FaceMesh(
        max_num_faces= max_num_faces, 
        refine_landmarks= redefine_landmarks, 
        min_detection_confidence= min_detection_confidence, 
        min_tracking_confidence= min_tracking_confidence,
        static_image_mode= static_image_mode
    )

#include "OpenCvHelper.hpp"
#include "CameraDistanceCalculator.hpp"

/**
 * shape_predictor_68_face_landmarks.dat modèle de détection des points du visage
 *
 */

/**
 * gestion de log des erreurs
 * @param error le message d'erreur
 */
void errorLog(std::string error){
    std::cerr << error << std::endl;
}

/**
 * lance tests opencv
 */
void openCvTests(){
    auto manager = new OpenCvHelper({
        "resources/images/1.jpeg",
        "resources/images/2.jpeg",
        "resources/images/3.jpeg",
        "resources/images/4.jpeg",
        "resources/images/5.jpeg",
        "resources/images/6.jpeg"
    },errorLog);

    // détection du visage
    {
        manager
                ->faceZonesDetection(OpenCvHelper::TestConfig::FROM_CAMERA)
                ->faceZonesDetection(OpenCvHelper::TestConfig::FROM_IMAGES);
    }

    // détection de marqueurs
    {
        manager
                ->markersDetection(OpenCvHelper::TestConfig::FROM_CAMERA)
                ->markersDetection(OpenCvHelper::TestConfig::FROM_IMAGES);
    }

    // détection de la distance par rapport à la caméra
    {
        manager
                ->distanceDetection(OpenCvHelper::TestConfig::FROM_CAMERA)
                ->distanceDetection(OpenCvHelper::TestConfig::FROM_IMAGES);
    }
}

/**
 * enregistre les données d'images pour un futur entrainement
 */
void registerCameraDistanceCalculatorImages(){
    CameraDistanceCalculator::registerTestImages("resources/calculator-network/",errorLog);
}

/**
 * lance l'entrainement du réseau de calcul de distance
 */
void trainCameraDistanceCalculator(){
    CameraDistanceCalculator::trainCalculator("resources/calculator-network/",errorLog);
}

int main(){
    registerCameraDistanceCalculatorImages();
    trainCameraDistanceCalculator();
//    openCvTests();

    return 0;
}
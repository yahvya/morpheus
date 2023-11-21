#include "opencv2/opencv.hpp"

/**
 * https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html
 * https://www.rapidtables.com/convert/color/rgb-to-hsv.html
 * https://www.datacamp.com/tutorial/face-detection-python-opencv
 */

/**
 * nom de la fenêtre d'affichage
 */
#define WINDOW_TITLE "Resultats"
/**
 * 1 pour conserver le ratio
 */
#define DP 1
/**
 * distance minimum entre le centre de 2 cercles (px)
 */
#define MIN_DIST 2
/**
 * d'après les recherche param1 est utilisé pour détecter les bords de l'image (pour une image claire 120 à 200 sont recommandés sinon 50 à 100 pour de petits cercles ...)
 */
#define IMAGE_QUALITY 200
/**
 * valeur plus il est petit plus de faux cercles peuvent être détecté on baisse un peu pour permettre les petits cercle
 */
#define DETECTION_PRECISION 20
/**
 * rayon minimum pixel
 */
#define MIN_RADIUS 1
/**
 * rayon maximum
 */
#define MAX_RADIUS 60
/**
 * caméra utilisée
 */
#define CAMERA 0
/**
 * touche de fermeture de la fenêtre
 */
#define ESCAPE_KEY 27
/**
 * facteur de réduction de l'image pour faciliter la détection
 */
#define REDUCT_SCALE 1.1
/**
 * Définition trouvé :
 * Dans un premier temps, le classificateur capturera un grand nombre de faux positifs. Ceux-ci sont éliminés à l'aide du paramètre minNeighbors, qui spécifie le nombre de rectangles voisins qui doivent être identifiés pour qu'un objet soit considéré comme une détection valide.
 * Spécifie le nombre de rectangles voisins qui doivent être identifiés pour qu'un objet soit considéré comme une détection valide
 * valeur à régler pour éliminer les faux positifs et garder les bons positifs
 */
#define MIN_NEIGHBORS 5
/**
 * listes des modèles téléchargé utilisable
 * https://github.com/opencv/opencv/blob/3.4/data/haarcascades/haarcascade_frontalface_default.xml
 * https://github.com/opencv/opencv/blob/3.4/data/haarcascades/haarcascade_profileface.xml
 * https://github.com/opencv/opencv/blob/3.4/data/haarcascades/haarcascade_smile.xml (celui ci peut être intéressant pour la bouche)
 */
#define MODELS_FILEPATH {"frontal-face.xml","profile-face.xml","smile.xml"}

/**
 * test à partir de la caméra
 */
void testFromCamera(){
    // intervalle de couleur recherché
    cv::Scalar colorInterval[] = {cv::Scalar(0,100,100),cv::Scalar(179, 255, 255)};

    // image de test,sortie de la recherche de couleur, et de frame de sorties hsv
    cv::Mat frame,mask,changedColorFrame;

    // données des cercles trouvés
    std::vector<cv::Vec3f> foundedCircles;

    // données détectés
    std::vector<cv::Rect> detectedRects;

    auto camera = cv::VideoCapture(CAMERA);

    if(!camera.isOpened() ){
        std::cerr << "Caméra non disponible" << std::endl;
        return;
    }

    // chargement des models de vérification
    std::vector<cv::CascadeClassifier> classifiers{};

    for(auto path : MODELS_FILEPATH) classifiers.push_back(cv::CascadeClassifier(path) );

    cv::namedWindow(WINDOW_TITLE,cv::WindowFlags::WINDOW_GUI_NORMAL);

    while(true){
        if(!camera.read(frame) ) continue;

        foundedCircles.clear();

        // on met l'image à l'endroit
        cv::flip(frame,frame,1);

        // recherche dans l'intervalle de couleur
        cv::cvtColor(frame,changedColorFrame,cv::COLOR_RGB2HSV);
        cv::inRange(changedColorFrame,colorInterval[0],colorInterval[1],mask);

        // recherche des pastilles de marquage
        cv::HoughCircles(
            mask,
            foundedCircles,
            cv::HOUGH_GRADIENT,
            DP,
            MIN_DIST,
            IMAGE_QUALITY,
            DETECTION_PRECISION,
            MIN_RADIUS,
            MAX_RADIUS
        );

        // recherche du visage
        cv::cvtColor(frame,changedColorFrame,cv::COLOR_RGB2GRAY);

        for(auto classifier : classifiers){
            classifier.detectMultiScale(
                    changedColorFrame,
                    detectedRects,
                    REDUCT_SCALE,
                    MIN_NEIGHBORS
            );

            // dessin des rectangles récupérés
            for(auto rect : detectedRects) cv::rectangle(frame,rect,cv::Scalar(0, 0, 255), 2);

            detectedRects.clear();
        }

        // marquage des cercles
        for(cv::Vec3i circleData : foundedCircles){
            cv::Point center(circleData[0],circleData[1]);

            // on place un point au centre du cercle
            cv::circle(frame,center,1,cv::Scalar(255,0,255),3,cv::LINE_AA);
            // on entoure le cercle
//            cv::circle(frame,center,circleData[2],cv::Scalar(0,100,100),3,cv::LINE_AA);
        }

        cv::imshow(WINDOW_TITLE,frame);

        if(cv::waitKey(1) == ESCAPE_KEY) break;
    }

    camera.release();
    cv::destroyAllWindows();
}

int main(){
    testFromCamera();

    return 0;
}
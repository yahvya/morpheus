//
// Created by devel on 30/11/2023.
//

#include "OpenCvHelper.hpp"

const char* OpenCvHelper::IMAGE_WINDOW_NAME = "Resultats images";
const char* OpenCvHelper::CAMERA_WINDOW_NAME = "Resultats camera";

OpenCvHelper::OpenCvHelper(std::vector<std::string> resources, void (errorLogger)(std::string) ) : errorLogger(errorLogger),resources(resources) {}

OpenCvHelper* OpenCvHelper::distanceDetection(OpenCvHelper::TestConfig from) {
    return this;
}

OpenCvHelper* OpenCvHelper::faceZonesDetection(TestConfig from){
    return this;
}

OpenCvHelper* OpenCvHelper::markersDetection(TestConfig from){
    cv::Mat frame;

    switch(from){
        case TestConfig::FROM_IMAGES:
            cv::namedWindow(OpenCvHelper::IMAGE_WINDOW_NAME,cv::WINDOW_NORMAL);

            for(auto& imagePath : this->resources){
                // lecture de l'image
                frame = cv::imread(imagePath);

                if(frame.data == nullptr){
                    this->errorLogger("Echec de lecture de l'image '" + imagePath + "'");
                    continue;
                }

                OpenCvHelper::detectMarkersIn(frame);

                cv::imshow(OpenCvHelper::IMAGE_WINDOW_NAME,frame);
                cv::waitKey();
            }
            ; break;

        case TestConfig::FROM_CAMERA:
            auto camera = cv::VideoCapture(0 );

            if(!camera.isOpened() ){
                this->errorLogger("Echec d'ouverture de la caméra");

                return this;
            }

            // touche espace pour quitter
            do{
                camera.read(frame);

                if(frame.data == nullptr) continue;

                // remise de l'image à l'endroit
                cv::flip(frame,frame,1);

                OpenCvHelper::detectMarkersIn(frame);
                cv::imshow(OpenCvHelper::CAMERA_WINDOW_NAME,frame);
            }
            while(cv::waitKey(100) != 32);

            camera.release();
        ; break;
    }

    cv::destroyAllWindows();

    return this;
}

void OpenCvHelper::detectMarkersIn(cv::Mat& frame){
    std::vector<cv::Vec3f> foundedCircles;
    cv::Mat mask,changedColorFrame;

    // conversion en matrice hsv facilitant la recherche
    cv::cvtColor(frame,changedColorFrame,cv::COLOR_RGB2HSV);
    // recherche par couleur (pour le test on inclus toutes les couleurs)
    cv::inRange(frame,cv::Scalar(0,0,0),cv::Scalar(179, 255, 255),mask);

    cv::HoughCircles(
            mask,
            foundedCircles,
            cv::HOUGH_GRADIENT,
            4, // ratio
            10, // distance min entre le centre de deux détections potentielles
            350, // sensibilité de détection
            35, // précision de détection
            1, // rayon minimum
            12 // rayon maximimum
    );

    for(cv::Vec3i circleData : foundedCircles){
        cv::Point center(circleData[0],circleData[1]);

        // on entoure le cercle
        cv::circle(frame,center,circleData[2],cv::Scalar(255,0,255),1,cv::LINE_AA);
    }

    std::cout << "nombre de résultats " << foundedCircles.size() << std::endl;
}
//
// Created by devel on 30/11/2023.
//

#ifndef TEST_OPENCV_OPENCVHELPER_HPP
#define TEST_OPENCV_OPENCVHELPER_HPP

#include <string>
#include <vector>
#include <functional>
#include "opencv2/opencv.hpp"

/**
 * helper opencv
 */
class OpenCvHelper {
    // types

    public:
        /**
        * défini sur quel support les ressources des tests sont tirés
        */
        enum TestConfig{FROM_CAMERA,FROM_IMAGES};

    public:
        /**
         * @param resources liste des chemins ressources image
         * @param errorLogger gestionnaire des messages d'erreur
         */
        explicit OpenCvHelper(std::vector<std::string> resources, void (errorLogger)(std::string) );

        /**
        * détection des points du visage
        * @param from source
         * @return this
        */
        OpenCvHelper* faceZonesDetection(TestConfig from);

        /**
        * détection de la distance par rapport à la caméra
        * @param from source
         * @return this
        */
        OpenCvHelper* distanceDetection(TestConfig from);

        /**
        * détection des marqueurs
        * @param from source
         * @return this
        */
        OpenCvHelper* markersDetection(TestConfig from);

        /**
        * détecte les marqueurs dans la frame fournie
        * @param frame frame
         * @return void
        */
        static void detectMarkersIn(cv::Mat& frame);

    // attributs

    protected:
        /**
         * fonction de log des erreurs
         */
        std::function<void(std::string)> errorLogger;

        std::vector<std::string> resources;

        /**
         * nom des fenêtres de tests sur images
         */
        static const char* IMAGE_WINDOW_NAME;

        /**
         * nom des fenêtres de tests sur caméra
         */
        static const char* CAMERA_WINDOW_NAME;
};


#endif //TEST_OPENCV_OPENCVHELPER_HPP

//
// Created by devel on 30/11/2023.
//

#ifndef TEST_OPENCV_CAMERADISTANCECALCULATOR_HPP
#define TEST_OPENCV_CAMERADISTANCECALCULATOR_HPP

#include <string>
#include <filesystem>
#include "Neuron.hpp"
#include "opencv2/opencv.hpp"

/**
 * calculateur de distance d'un visage trouvé par rapport à la caméra
 */
class CameraDistanceCalculator {
    // types
    public:
        /**
         * défini la position du visage dans l'image
         */
        enum PositionConfig{
            /**
             * de profil
             * @criteria
             */
            PROFILE = 1,
            /**
             * de face
             * @criteria distance entre les yeux
             */
            FACE
        };

        /**
         * configuration d'une image
         */
        typedef struct ImageConfig{
            public:
                /**
                 * distance défini pour l'image
                 */
                double distance;
                /**
                 * valeur calculé du critère de vérification en fonction de la position
                 */
                double criteria;
                /**
                 * position de la personne dans l'image
                 */
                PositionConfig position;

                /**
                 *
                 * @param distance distance défini pour l'image
                 * @param position position de la personne dans l'image
                 * criteria à -1 par défaut
                 */
                ImageConfig(float distance,PositionConfig position) : distance(distance), position(position), criteria(-1){}
        }ImageConfig;

        /**
         * définition d'une couche
         */
        typedef std::vector<Neuron*> Layer;

    public:
            /**
             * @param configDirPath chemin du dossier de configuration du réseau
             * @param loadImagesConfig si les configurations des images doivent être chargés
             */
            explicit CameraDistanceCalculator(std::filesystem::path configDirPath,bool loadImagesConfig);

            /**
             * initialise les couches du réseau
             * @param countOfLayers nombre de couches
             * @param inputSize nombre de neurones sur une couche
             * @return this
             */
            CameraDistanceCalculator* initLayers(int countOfLayers,int layersSize);

            /**
             * récupère le critère calculé à partir de la position
             * @param config configuration image sans criteria de forcément défini
             * @param imagePath chemin de l'image
             * @return la valeur critère
             * @throw runtime_error en cas d'erreur
             */
            static double getCriteriaFrom(ImageConfig config,std::string imagePath);

            /**
             * récupère le critère calculé à partir de la position
             * @param config configuration image sans criteria de forcément défini
             * @param frame frame de l'image
             * @return la valeur critère
             * @throw runtime_error en cas d'erreur
             */
            static double getCriteriaFrom(ImageConfig config,cv::Mat frame);

        // fonctions d'entrainement

        /**
         * enregistre un groupe d'image d'entrainement pour un type de caméra
         * @param resourcesPath chemin du dossier ressources destiné au réseau
         * @param errorLogger gestionnaire des messages erreurs
         */
        static void registerTestImages(std::string resourcesPath,void (errorLogger)(std::string) );

        /**
         * lance un entrainement
         * @param resourcesPath chemin du dossier ressources destiné au réseau
         * @param errorLogger gestionnaire des messages erreurs
         */
        static void trainCalculator(std::string resourcesPath,void (errorLogger)(std::string));

    protected:
        /**
         * charge les données du réseau
         * @param loadImagesConfig si les configurations des images doivent être chargés
         * @return si le chargement à réussi
         */
        bool load(bool loadImagesConfig);

    // attributs

    protected:
        /**
         * chemin du dossier de configuration du réseau
         */
        std::filesystem::path configDirPath;

        /**
         * configuration des images d'entrainement si chargé
         */
        std::vector<ImageConfig> imagesConfig;

        /**
         * couche du réseau
         */
        std::vector<Layer*> layers;

        Layer* outputLayer;

        /**
         * extension des fichiers network
         */
        static const char* NETWORK_FILE_EXTENSION;

        /**
         * détecteur des yeux
         */
        static cv::CascadeClassifier* EYES_DETECTOR;

        /**
         * détecteur à changer
         */
        static cv::CascadeClassifier* TMP_DETECTOR;
};

#endif //TEST_OPENCV_CAMERADISTANCECALCULATOR_HPP

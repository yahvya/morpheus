//
// Created by devel on 30/11/2023.
//

#include <fstream>
#include <sstream>
#include <iostream>
#include <exception>
#include <cmath>
#include "CameraDistanceCalculator.hpp"

/**
 * vérifie une condition ou affiche le message d'erreur avant de quitter la fonction
 * @param cond la condition
 * @param errorMessage le message d'erreur
 */
#define COND_OR_ERROR(cond,errorMessage) \
    if(cond){ \
        errorLogger(errorMessage); \
        return; \
    }

/**
 * vérifie une condition ou affiche le message d'erreur, supprime le dossier crée avant de quitter la fonction
 * @param cond la condition
 * @param errorMessage le message d'erreur
 */
#define CHECK_OR_ERASE(cond,errorMessage) \
    if(cond){\
        errorLogger(errorMessage);\
        std::filesystem::remove_all(path);\
        return;\
    }

/**
 * emmène le fichier jusqu'au texte fourni
 * @param file le fichier
 * @param in chaine de destination
 * @param to le texte
 */
#define GO_TO(file,in,to) \
    while(getline(file,in) && in != to);

const char* CameraDistanceCalculator::NETWORK_FILE_EXTENSION = ".nt-paoli";

cv::CascadeClassifier* CameraDistanceCalculator::EYES_DETECTOR = nullptr;
cv::CascadeClassifier* CameraDistanceCalculator::TMP_DETECTOR = nullptr;

/**
 * récupère le nombre d'élements dans un dossier
 * @param resourcesPath chemin du dossier
 * @return le nombre d'élement
 */
int getCountOfElementsIn(std::filesystem::path resourcesPath){
    auto it = std::filesystem::directory_iterator(resourcesPath);

    int count = 0;

    for(auto f : it) count++;

    return count;
}

CameraDistanceCalculator::CameraDistanceCalculator(std::filesystem::path configDirPath,bool loadImagesConfig) : configDirPath(configDirPath){
    // chargement des modèles de détection

    if(CameraDistanceCalculator::EYES_DETECTOR == nullptr){
        try{
            CameraDistanceCalculator::EYES_DETECTOR = new cv::CascadeClassifier(configDirPath.parent_path().parent_path().parent_path().string() + "/models/haarcascade_eye.xml");

            if(CameraDistanceCalculator::EYES_DETECTOR->empty() ) throw std::exception();
        }
        catch(std::exception&){
            throw std::runtime_error("Echec de chargement du modèle de détection des yeux");
        }
    }

    /*
    if(CameraDistanceCalculator::TMP_DETECTOR == nullptr){
        try{

        }
        catch(std::exception&){
            throw std::runtime_error("Echec de chargement du modèle de détection des yeux");
        }
    }
    */

    this->load(loadImagesConfig);
}

bool CameraDistanceCalculator::load(bool loadImagesConfig){
    if(!std::filesystem::exists(this->configDirPath) ) throw std::runtime_error("Le dossier de configuration fourni n'existe pas");

    std::ifstream networkFileReader(this->configDirPath.string() + "network" + CameraDistanceCalculator::NETWORK_FILE_EXTENSION);

    if(!networkFileReader.is_open() ) throw std::runtime_error("Echec de lecture du fichier de configuration du réseau");

    std::string line;

    if(loadImagesConfig){
        // chargement de la configuration de images
        GO_TO(networkFileReader,line,"[images]");

        getline(networkFileReader,line);

        std::string config;
        std::stringstream lineStream(line);

        while(getline(lineStream,config,'|') ){
            auto sepPos = config.find(';');
            auto imageName = config.substr(0,sepPos);

            config = config.substr(sepPos + 1);
            sepPos = config.find(';');

            ImageConfig imageConfig(
                std::stof(config.substr(0,sepPos ) ),
                static_cast<PositionConfig>(std::stoi(config.substr(sepPos + 1) ) )
            );

            try {
                // on récupère la valeur du critère en fonction de la position
                imageConfig.criteria = CameraDistanceCalculator::getCriteriaFrom(imageConfig,this->configDirPath.string() + "images/" + imageName);

                this->imagesConfig.push_back(imageConfig);
            }
            catch (std::exception& e){
                std::cerr << "Echec de récupération de la valeur critère pour l'image '" + imageName + "' ignoré - erreur : " << e.what() << std::endl;
            }
        }
    }

    // chargement du réseau
    GO_TO(networkFileReader,line,"[network]");



    return true;
}

CameraDistanceCalculator* CameraDistanceCalculator::initLayers(int countOfLayers,int layersSize){
    // création des neuronnes intermédiaires et affectation de la bonne taille
    this->layers = std::vector<Layer*>();
    this->layers.resize(countOfLayers);

    for(auto& layer : this->layers){
        layer->resize(layersSize);

        // affectation des poids par défaut
        for(auto& neuron : *layer) neuron->generateWeight();
    }

    this->outputLayer = new Layer();

    return this;
}

double CameraDistanceCalculator::getCriteriaFrom(ImageConfig config,std::string imagePath){
    auto frame = cv::imread(imagePath);

    if(frame.data == nullptr) throw std::runtime_error("Echec de transformation de l'image en frame");

    return CameraDistanceCalculator::getCriteriaFrom(config,frame);
}

double CameraDistanceCalculator::getCriteriaFrom(ImageConfig config,cv::Mat frame){
    std::vector<cv::Rect> foundedEyes;

    cv::Mat changedColorFrame;

    switch(config.position){
        case PositionConfig::FACE:
            // détection des yeux
            cv::cvtColor(frame,changedColorFrame,cv::COLOR_BGR2GRAY);

            CameraDistanceCalculator::EYES_DETECTOR->detectMultiScale(changedColorFrame,foundedEyes,1.2);

            if(foundedEyes.size() == 2){
                cv::Point center1 = {(foundedEyes[0].x + foundedEyes[0].width / 2, foundedEyes[0].y + foundedEyes[0].height / 2)};
                cv::Point center2 = {(foundedEyes[1].x + foundedEyes[1].width / 2, foundedEyes[1].y + foundedEyes[1].height / 2)};

                return sqrt((abs(center1.x - center2.x) )^2 + (abs(center1.y - center2.y) )^2);
            }

            throw std::runtime_error("Echec de détection des données sur les yeux images de face");
       ; break;

        case PositionConfig::PROFILE:
            throw std::runtime_error("Detection de profil à implémenter");
        ;break;
    }

    return -1;
}

void CameraDistanceCalculator::registerTestImages(std::string resourcesPath,void (errorLogger)(std::string) ){
    /**
     * structures du dossier resourcesPath\n\n
     *
     * dossier-1\n
     * - images\n
     * -- 1.jpg...\n
     * - network.nt-paoli\n\n
     *
     * dossier-2\n
     * - images\n
     * -- 1.jpg...\n
     * - network.nt-paoli
     */

    resourcesPath += "networks/";

    auto path = std::filesystem::path(resourcesPath);

    // vérification d'existance du dossier ou création du dossier
    if(!std::filesystem::exists(path) ) std::filesystem::create_directory(path);

    COND_OR_ERROR(!std::filesystem::exists(path),"Echec de création du dossier des ressources dans le chemin '" + resourcesPath + "'");

    // création du nouveau dossier
    std::string newDirPath = resourcesPath + "dossier-" + std::to_string(getCountOfElementsIn(path) + 1 ) + "/";

    path = std::filesystem::path(newDirPath);

    auto imagesPath = newDirPath + "images/";

    COND_OR_ERROR(!std::filesystem::create_directory(path),"Echec de création du nouveau dossier");
    COND_OR_ERROR(!std::filesystem::create_directory(std::filesystem::path(imagesPath) ),"Echec de création du dossier des images");

    std::string input;

    // enregistrement des images
    std::cout << "Veuillez saisir le chemin du fichier de configuration des images (au format chemin;distance;position (1 pour profil - 2 pour face)\\n...) : ";

    std::cin >> input;

    auto configFilePath = std::filesystem::path(input);

    CHECK_OR_ERASE(std::filesystem::file_size(configFilePath) == 0,"Le chemin fourni ne contient aucun chemin d'image");

    // lecture du fichier pour la copie des images et création du fichier network
    std::ifstream configFileReader(configFilePath);
    std::ofstream netWorkFileWriter(std::filesystem::path(newDirPath + "network" + CameraDistanceCalculator::NETWORK_FILE_EXTENSION) );

    CHECK_OR_ERASE(!configFileReader.is_open(),"Echec de lecture du fichier de configuration");
    CHECK_OR_ERASE(!netWorkFileWriter.is_open(),"Echec d'écriture du fichier network'");

    netWorkFileWriter << "[images]" << std::endl;

    for(int count = 1;std::getline(configFileReader,input);count++){
        auto firstSepPos = input.find(';');
        auto imageFilePath = std::filesystem::path(input.substr(0,firstSepPos) );
        auto imageFinalName = std::to_string(count) + imageFilePath.extension().string();

        netWorkFileWriter << imageFinalName << ";" << input.substr(firstSepPos + 1) << "|";

        // copie de l'image
        std::filesystem::copy_file(imageFilePath,std::filesystem::path(imagesPath + imageFinalName) );
    }

    netWorkFileWriter << std::endl << "[network]";

    configFileReader.close();
    netWorkFileWriter.close();
}

void CameraDistanceCalculator::trainCalculator(std::string resourcesPath,void (errorLogger)(std::string) ){
    resourcesPath += "networks/";

    COND_OR_ERROR(!std::filesystem::exists(std::filesystem::path(resourcesPath) ),"Le chemin fourni ne contient pas d'élements traitable");

    // récupération du dossier contenant le réseau à traiter
    auto it = std::filesystem::directory_iterator(std::filesystem::path(resourcesPath) );

    std::cout << "--- Liste des dossiers ---" << std::endl;

    for(auto& filename : it) std::cout << "\t" << filename.path().filename() << std::endl;

    std::cout << "Entrez le nom du dossier à traiter : ";

    std::string choosedFolder;

    std::cin >> choosedFolder;

    auto dirPath = std::filesystem::path(resourcesPath + choosedFolder + "/");

    COND_OR_ERROR(!std::filesystem::exists(dirPath),"Le dossier choisi n'existe pas");

    try{
        auto calculator = new CameraDistanceCalculator(dirPath,true);


    }
    catch(std::exception& e){
        errorLogger(e.what() );
    }
}
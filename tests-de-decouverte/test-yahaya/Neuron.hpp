//
// Created by devel on 01/12/2023.
//

#ifndef TEST_OPENCV_NEURON_HPP
#define TEST_OPENCV_NEURON_HPP

/**
 * neuronne de réseau de mesure de distance
 */
class Neuron {

    public:
        /**
         * fonction d'activation du neuronne
         * @param value valeur d'entrée
         * @return la valeur d'activation
         */
        double activate(double value);

        /**
         * met à jour le poids
         * @param learningRate taux d'apprentissage servant à la variation du poids
         * @param error l'erreur de remonté
         * @return this
         */
        Neuron* updateWeight(double learningRate,double error);

        /**
         * génére un poids aléatoire pour le neuronne
         * @return this
         */
        Neuron* generateWeight();

        /**
         *
         * @return le poids courant du neuronne
         */
        double getWeight();

    protected:
        /**
         * poids du neuronne
         */
        double weight;
};


#endif //TEST_OPENCV_NEURON_HPP

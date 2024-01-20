//
// Created by devel on 01/12/2023.
//

#include "Neuron.hpp"
#include <random>

/**
 * dans notre cas une fonction linéaire est plus intéressant
 */

double Neuron::activate(double value) {
    return value;
}

Neuron* Neuron::updateWeight(double learningRate,double error){
    this->weight += learningRate * error;

    return this;
}

Neuron *Neuron::generateWeight() {
    std::random_device random;

    this->weight = static_cast<float>(random() );

    return this;
}

double Neuron::getWeight() {
    return this->weight;
}
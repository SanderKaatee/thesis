import random
import numpy as np

class Perceptron:
    def __init__(self, input_size, output_classes):
        self.input_size = input_size
        self.output_classes = output_classes
        self.num_classes = len(output_classes)
        self.weights = np.zeros((self.num_classes, input_size))
        self.bias = np.zeros(self.num_classes)
    
    def predict(self, input_vector):
        weighted_sum = np.dot(self.weights, input_vector) + self.bias
        activation = self.activation_function(weighted_sum)
        return self.output_classes[activation]
    
    def train(self, training_data, learning_rate):
        for input_vector, target_output in training_data:
            target_vector = self.one_hot_encode(target_output)
            predicted_output = self.predict(input_vector)
            if predicted_output != target_output:
                predicted_vector = self.one_hot_encode(predicted_output)
                error = target_vector - predicted_vector
                self.update_weights(input_vector, error, learning_rate)
    
    def update_weights(self, input_vector, error, learning_rate):
        input_vector = np.array(input_vector)
        for i in range(self.num_classes):
            self.weights[i] += learning_rate * error[i] * input_vector
            self.bias[i] += learning_rate * error[i]
    
    def activation_function(self, weighted_sum):
        return np.argmax(weighted_sum)
    
    def one_hot_encode(self, target_output):
        target_vector = np.zeros(self.num_classes)
        target_vector[self.output_classes.index(target_output)] = 1
        return target_vector

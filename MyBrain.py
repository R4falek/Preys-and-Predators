import numpy as np
import random
from numba import jit


class MyBrain:
    def __init__(self, input_layer):
        self.input_layer_weights = np.zeros((input_layer + 1, 3))
        self.hidden_layer_weights = np.zeros((input_layer + 1, input_layer))
        self.output_layer_weights = np.zeros((input_layer, 3))
        self.model = [self.input_layer_weights, self.hidden_layer_weights, self.output_layer_weights]
        self.random_init()

    @staticmethod
    def sigmoid(x):
        for i in range(len(x)):
            x[i] = 1 / (1 + np.exp(-x[i]))
        return x

    @staticmethod
    def relu(x):
        for i in range(len(x)):
            x[i] = max(0, x[i])
        return x

    def forward(self, input_vector):
        input_with_bias = np.append(input_vector, [1])

        first_layer_output = np.dot(input_with_bias, self.hidden_layer_weights)
        first_layer_output = self.relu(first_layer_output)

        second_layer_output = np.dot(first_layer_output, self.output_layer_weights)
        second_layer_output = self.relu(second_layer_output)

        o = np.dot(input_with_bias, self.input_layer_weights)
        o = self.relu(o)

        return self.sigmoid(second_layer_output + o)

    def modify_weights(self, modify_chance):
        if random.random() < modify_chance:
            layer = random.randint(0, 2)
            i = random.randint(0, len(self.model[layer]) - 1)
            j = random.randint(0, len(self.model[layer][i]) - 1)
            self.model[layer][i][j] = random.uniform(-1, 1)

        # for layer in range(len(self.model)):
        #     for i in range(len(self.model[layer])):
        #         for j in range(len(self.model[layer][i])):
        #             if modify_chance > random.random():
        #                 self.model[layer][i][j] = random.uniform(-1, 1)

    def random_init(self):
        for layer in range(len(self.model)):
            for i in range(int(len(self.model[layer]))):
                for j in range(int(len(self.model[layer][i]))):
                    if random.random() < 0.5:
                        self.model[layer][i][j] = random.uniform(-1, 1)

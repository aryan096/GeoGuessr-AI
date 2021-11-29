import tensorflow as tf
from tensorflow.keras.layers import \
    Conv2D, MaxPool2D, Dropout, Flatten, Dense

import hyperparameters as hp
import numpy as np

class GeoLocationCNN(tf.keras.Model):
    """ Geolocation using CNNs """

    def __init__(self):
        super(GeoLocationCNN, self).__init__()

        # OPTIMIZER       
        self.learning_rate = 0.1      
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

        self.architecture = [
              Conv2D(128, 3, 1, padding="same",
                     activation="relu"),
              MaxPool2D(3),
              Conv2D(128, 3, 1, padding="same",
                     activation="relu"),
              MaxPool2D(3),
              Conv2D(256, 3, 1, padding="same",
                     activation="relu"),
              MaxPool2D(3),
              Dropout(0.4),
              Dense(32),
              Flatten(),
              Dense(15, activation='softmax')
        ]

    def call(self, x):
        """ Passes input image through the network. """

        for layer in self.architecture:
            x = layer(x)

        return x

    @staticmethod
    def loss_fn(labels, predictions):
        """ Loss function for the model. """

        cce = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        return cce(labels, predictions)
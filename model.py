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
        self.learning_rate = 0.001 
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

        self.vgg16 = [
            # Block 1
            Conv2D(64, 3, 1, padding="same",
                   activation="relu", name="block1_conv1"),
            Conv2D(64, 3, 1, padding="same",
                   activation="relu", name="block1_conv2"),
            MaxPool2D(2, name="block1_pool"),
            # Block 2
            Conv2D(128, 3, 1, padding="same",
                   activation="relu", name="block2_conv1"),
            Conv2D(128, 3, 1, padding="same",
                   activation="relu", name="block2_conv2"),
            MaxPool2D(2, name="block2_pool"),
            # Block 3
            Conv2D(256, 3, 1, padding="same",
                   activation="relu", name="block3_conv1"),
            Conv2D(256, 3, 1, padding="same",
                   activation="relu", name="block3_conv2"),
            Conv2D(256, 3, 1, padding="same",
                   activation="relu", name="block3_conv3"),
            MaxPool2D(2, name="block3_pool"),
            # Block 4
            Conv2D(512, 3, 1, padding="same",
                   activation="relu", name="block4_conv1"),
            Conv2D(512, 3, 1, padding="same",
                   activation="relu", name="block4_conv2"),
            Conv2D(512, 3, 1, padding="same",
                   activation="relu", name="block4_conv3"),
            MaxPool2D(2, name="block4_pool"),
            # Block 5
            Conv2D(512, 3, 1, padding="same",
                   activation="relu", name="block5_conv1"),
            Conv2D(512, 3, 1, padding="same",
                   activation="relu", name="block5_conv2"),
            Conv2D(512, 3, 1, padding="same",
                   activation="relu", name="block5_conv3"),
            MaxPool2D(2, name="block5_pool")
        ]

        for layer in self.vgg16:
               layer.trainable = False

        self.head = [ 
               # Conv2D(512, 3, 1, padding="same", activation="relu"),
               # Conv2D(512, 3, 1, padding="same", activation="relu"),
               # MaxPool2D(2),
               Flatten(),
              #  Dense(512, activation="relu"),
               Dense(64, activation="relu"),
               Dense(89, activation="softmax")
        ]

       #  self.vgg16 = tf.keras.Sequential(self.vgg16, name="vgg_base")
        self.head = tf.keras.Sequential(self.head, name="vgg_head")

    def call(self, x):
        """ Passes input image through the network. """
        print("call")
       #  x = self.vgg16(x)
        print("all")
        x = self.head(x)
        print("the")
       
        return x

    @staticmethod
    def loss_fn(labels, predictions):
        """ Loss function for the model. """
        print("monsters")
        loss = tf.keras.losses.sparse_categorical_crossentropy(labels, predictions)
        return loss
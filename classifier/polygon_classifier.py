import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
import numpy as np


class PolygonClassifier:
    def __init__(self, input_shape, num_classes=2):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None

    def setup(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        modelpath = os.path.join(curpath, "polymodel")
        if os.path.isfile(modelpath):
            self.model = keras.models.load_model(modelpath)
            print("Loading model from: %s" % modelpath)
        else:
            self.model = self.create_model()
            print("Creating new model.")

    def create_model(self):
        self.model = tf.keras.Sequential(
            [
                keras.Input(shape=self.input_shape),
                layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Flatten(),
                layers.Dropout(0.5),
                layers.Dense(self.num_classes, activation="softmax"),
            ]
        )

        self.model.summary()

    def train_model(self, images, labels):
        batch_size = 20
        epochs = 10

        self.model.compile(
            loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
        )
        self.model.fit(
            images, labels, batch_size=batch_size, epochs=epochs, validation_split=0.1
        )

    def evaluate(self, images):
        pass

    def save_model(self, location):
        curpath = os.path.dirname(os.path.realpath(__file__))
        modelpath = os.path.join(curpath, "polymodel")
        self.model.save(modelpath)
        print("Saving model at: %s" % modelpath)

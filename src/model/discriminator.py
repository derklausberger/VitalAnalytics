import tensorflow.keras
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense, Flatten

import numpy as np

class Discriminator:
    '''def __init__(self, X_train=None, y_train=None, latent_dim=102, data_dim=2, sequence_length=650000):
        self.latent_dim = latent_dim
        self.sequence_length = sequence_length
        self.data_dim = data_dim
        
        if X_train is not None and y_train is not None:
            self.X_train = X_train
            self.y_train = y_train

        self.model = self.build()'''

    def __init__(self, sequence_length=650000, data_dim=2):
        self.sequence_length = sequence_length
        self.data_dim = data_dim
        self.model = self.build()

    def build(self):
        print("building discriminator...")

        input_layer = Input(shape=(self.sequence_length, self.data_dim))
        x = Flatten()(input_layer)
        x = Dense(128, activation="relu")(x)
        
        # Ausgaben für real/fake und afib class
        real_fake_output = Dense(1, activation="sigmoid", name="real_or_fake")(x)
        afib_class_output = Dense(1, activation="sigmoid", name="afib_class")(x)

        model = Model(inputs=input_layer, outputs=[real_fake_output, afib_class_output])

        # Kompiliere das Modell mit 2 Losses
        model.compile(
            loss={
                "real_or_fake": "binary_crossentropy",
                "afib_class": "binary_crossentropy"
            },
            optimizer="adam",
            metrics={
                "real_or_fake": ['accuracy'],
                "afib_class": ['accuracy']
            }
        )

        #model.summary()
        return model
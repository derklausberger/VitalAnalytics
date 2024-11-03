import tensorflow.keras as keras
from tensorflow.keras import Input, Sequential, Model
from tensorflow.keras.layers import Dense, Reshape

import numpy as np

class Generator:
    def __init__(self, latent_dim=102, data_dim=2, sequence_length=650000):
        self.latent_dim = latent_dim
        self.sequence_length = sequence_length
        self.data_dim = data_dim
        
        '''if X_train is not None and y_train is not None:
            self.X_train = X_train
            self.y_train = y_train'''

        self.model = self.build()

    def build(self):
        print("building generator...")

        # Eingabe des latenten Vektors
        input_noise = Input(shape=(self.latent_dim,))

        # Hauptnetzwerk für generierte Sequenzdaten
        x = Dense(self.sequence_length * self.data_dim, activation='sigmoid')(input_noise)
        sequence_output = Reshape((self.sequence_length, self.data_dim))(x)

        # Zweiter Output für afib-Label, z.B. durch eine zusätzliche Dense-Schicht
        afib_output = Dense(1, activation='sigmoid', name="afib_class")(input_noise)  # Binäres afib-Label

        # Modell mit zwei Outputs erstellen
        model = Model(inputs=input_noise, outputs=[sequence_output, afib_output])

        return model

    def save_to_file(self, file_name='generator.keras'):
        self.model.save(file_name)

    def generate_samples(self, num_samples=5):
        print("generating samples...")
        noise = np.random.normal(0, 1, (num_samples, 102))
        return self.model.predict(noise)

    @staticmethod
    def load_from_file(file_name, latent_dim=102, data_dim=2, sequence_length=650000):
        print(f"Loading generator model from {file_name}...")
        loaded_model = keras.models.load_model(file_name)
        
        generator = Generator(latent_dim=latent_dim, data_dim=data_dim, sequence_length=sequence_length)
        
        generator.model = loaded_model
        return generator
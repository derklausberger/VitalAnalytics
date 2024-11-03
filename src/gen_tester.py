import numpy as np
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense, Flatten

# Beispiel: Discriminator Klasse
class Discriminator:
    def __init__(self, sequence_length=650000, data_dim=2):
        self.sequence_length = sequence_length
        self.data_dim = data_dim
        self.model = self.build()

    def build(self):
        input_layer = Input(shape=(self.sequence_length, self.data_dim))
        x = Flatten()(input_layer)
        x = Dense(128, activation="relu")(x)
        
        # Ausgaben für real/fake und afib class
        real_fake_output = Dense(1, activation="sigmoid", name="real_or_fake")(x)
        afib_class_output = Dense(1, activation="sigmoid", name="afib_class")(x)

        model = Model(inputs=input_layer, outputs=[real_fake_output, afib_class_output])

        # Kompiliere das Modell mit Verlusten
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

        model.summary()

        return model

# Trainingsdaten simulieren
X_train = np.random.rand(16, 650000, 2)  # Simulierte Eingabedaten
y_train = np.random.randint(0, 2, size=(16, 1))  # Simulierte Labels für AFib

# Trainingsfunktion
def train(discriminator, X_train, y_train, epochs=10, batch_size=4):
    half_batch = batch_size // 2

    for epoch in range(epochs):
        idx = np.random.randint(0, X_train.shape[0], half_batch)

        real_labels = np.ones((half_batch, 1))
        real_afib_labels = y_train[idx].reshape(-1, 1)

        real_labels_combined = {
            "real_or_fake": real_labels,
            "afib_class": real_afib_labels
        }

        # Trainiere den Discriminator
        d_loss_real = discriminator.model.train_on_batch(X_train[idx], real_labels_combined)
        print(f"Epoch {epoch}, D Loss: {d_loss_real}")

# Discriminator erstellen und trainieren
discriminator = Discriminator()
train(discriminator, X_train, y_train)

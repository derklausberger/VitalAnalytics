import os
import numpy as np
from tensorflow.keras import Input, Sequential, Model
from tensorflow.keras.layers import Dense, Reshape
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.keras.callbacks import ModelCheckpoint

from model.generator import Generator
from model.discriminator import Discriminator


checkpoint_dir = "checkpoints"
os.makedirs(checkpoint_dir, exist_ok=True)

# Initialisiere den Checkpoint für den Generator
generator_checkpoint = ModelCheckpoint(
    filepath=os.path.join(checkpoint_dir, "generator_checkpoint.keras"),
    save_best_only=True,         # Speichert nur das beste Modell
    monitor="g_loss",            # Verfolge die Generator-Loss während des Trainings
    mode="min",                  # Speichere das Modell, wenn der Loss minimiert wird
    save_weights_only=False      # Speichere das gesamte Modell, nicht nur die Gewichte
)

discriminator_checkpoint = ModelCheckpoint(
    filepath=os.path.join(checkpoint_dir, "discriminator_checkpoint.keras"),
    save_best_only=True,
    monitor="d_loss",
    mode="min",
    save_weights_only=False
)


class GAN:
    def __init__(self, X_train, y_train, latent_dim=102, data_dim=2, sequence_length=650000):
        print("initalizing GAN...")
        self.X_train = X_train
        self.y_train = y_train

        self.latent_dim = latent_dim
        self.data_dim = data_dim
        self.sequence_length = sequence_length

        self.encode_labels()

        self.discriminator = Discriminator()#X_train=X_train, y_train=y_train)#self.build_discriminator()
        self.generator = Generator()#X_train=X_train, y_train=y_train)#self.build_generator()
        self.model = self.build_gan()

        self.gan.fit(
            callbacks=[generator_checkpoint, discriminator_checkpoint],  # Füge die Checkpoints hinzu
            epochs=1,
            
        )

    def build_gan(self):
        print("building gan...")
        self.discriminator.model.trainable = False  # Diskriminator nicht trainierbar

        input_noise = Input(shape=(self.latent_dim,))

        generated_data, generated_afib_label = self.generator.model(input_noise)
        
        # Diskriminator gibt zwei Ausgaben zurück
        validity, afib_class = self.discriminator.model(generated_data)

        model = Model(input_noise, [validity, afib_class])  # Mehrere Ausgaben

        model.compile(
            loss=['binary_crossentropy', 'binary_crossentropy'],  # Verluste für beide Ausgaben
            optimizer=Adam(0.0002, 0.5)
        )
        return model

    def encode_labels(self):
        label_encoder = LabelEncoder()
        self.y_train = label_encoder.fit_transform(self.y_train)

    def get_onehot_labels(self):
        onehot_encoder = OneHotEncoder(sparse_output=False)
        encoded_labels = self.y_train.reshape(len(self.y_train), 1)
        onehot_labels = onehot_encoder.fit_transform(encoded_labels)

        return onehot_labels

    '''def get_sampled_labels_onehot(self, batch_size=64):
        sampled_labels = np.random.randint(0, 2, (batch_size, 1))
        sampled_labels_onehot = to_categorical(sampled_labels, num_classes=2)
        return sampled_labels_onehot'''

    def get_noise(self, batch_size=64):
        return np.random.normal(0, 1, (batch_size, self.latent_dim))

    def train(self, epochs=10, batch_size=4):
        print("training gan...")
        half_batch = batch_size // 2
        #X_train = np.random.rand(16, 650000, 2)  # Beispiel-Daten
        #y_train = np.random.randint(0, 2, size=(16, 1))

        try:
            for epoch in range(epochs):
                self.discriminator.model.trainable = True

                # train discriminator using real data
                idx = np.random.randint(0, X_train.shape[0], half_batch)
                
                real_labels = np.ones((half_batch, 1))
                real_afib_labels = y_train[idx].reshape(-1, 1)

                real_labels_combined = {
                    "real_or_fake": real_labels,
                    "afib_class": real_afib_labels
                }

                d_loss_real = self.discriminator.model.train_on_batch(X_train[idx], real_labels_combined)               
                
                

                # train discriminator on fake data
                fake_labels = np.zeros((half_batch, 1))

                noise = self.get_noise(half_batch)
                generated_data, fake_afib_labels = self.generator.model(noise)

                # MUSS ICH SPÄTER NOCH ERSETZEN!!!
                #fake_afib_labels = np.random.randint(0, 2, size=(half_batch, 1))

                fake_labels_combined = {
                    "real_or_fake": fake_labels,
                    "afib_class": fake_afib_labels
                }

                d_loss_fake = self.discriminator.model.train_on_batch(generated_data, fake_labels_combined)



                d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
                # sampled_labels = np.random.randint(0, 2, (batch_size, 1))
                # sampled_labels_onehot = to_categorical(sampled_labels, num_classes=2)

                # train generator to play discriminator
                valid = np.ones((batch_size, 1))
                g_loss = self.model.train_on_batch(noise, valid)  # , sampled_labels_onehot

                print(f"Epoch {epoch}, D Loss: {d_loss}, G Loss: {g_loss}")
        except Exception as e:
            print(f"Error during training: {e}")

            #print(f"X_train shape: {self.X_train[idx].shape}")
            #print(f"real_labels shape: {real_labels.shape}")
            #print(f"real_afib_labels shape: {real_afib_labels.shape}")
            #print(f"combined labels shape: {real_labels_combined['real_or_fake'].shape}, {real_labels_combined['afib_class'].shape}")

            #self.discriminator.model.summary()

            os._exit(0)


    # GENERATOR
    def generate_samples(self, num_samples=5):
        self.generator.generate_samples(num_samples);
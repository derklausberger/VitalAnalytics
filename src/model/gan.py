import keras.models
import numpy as np

from keras import Input, Sequential
from keras.layers import Dense, Reshape
from keras.optimizers import Adam
from keras.utils import to_categorical
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


class GAN:
    def __init__(self, X_train, y_train, latent_dim=100, data_dim=2, sequence_length=650000):
        print("initalizing GAN...")
        self.X_train = X_train
        self.y_train = y_train

        self.latent_dim = latent_dim
        self.data_dim = data_dim
        self.sequence_length = sequence_length

        self.encode_labels()

        self.discriminator = self.build_discriminator()
        self.generator = self.build_generator()
        self.gan = self.build_gan()

    def build_generator(self):
        print("building generator...")
        # X_train.shape = (25, 650000, 2,)
        # y_train.shape = (25,)
        model = Sequential()
        # model.add(Input(shape=(self.sequence_length, self.data_dim)))
        model.add(Input(shape=(102,)))
        model.add(Dense(650000 * 2, activation='sigmoid'))
        model.add(Reshape((650000, 2)))
        return model
        '''input_noise = Input(shape=(self.latent_dim,)) # shape = (None,100)
        input_label = Input(shape=(self.sequence_length, self.data_dim)) # shape = (None, 650000,2)

        merged_input = Concatenate(axis=-1)([input_noise, input_label])

        x = Dense(64)(Flatten()(merged_input))
        x = LeakyReLU(alpha=0.2)(x)
        x = LSTM(self.data_dim, return_sequences=True)(x)
        model = Model([input_noise, input_label], x)
        return model'''

    def build_discriminator(self):
        print("building discriminator...")
        model = Sequential()
        model.add(Input((self.sequence_length, self.data_dim,)))
        #model.add(Input(shape=(2,)))
        model.add(Dense(1))
        return model
        '''input_data = Input(shape=(self.sequence_length, self.data_dim))
        input_label = Input(shape=(1,))

        x = Embedding(2, 50)(input_label)
        label_embedding = Flatten()(x)

        label_embedding_repeated = RepeatVector(self.sequence_length)(label_embedding)
        merged_input = Concatenate(axis=2)([input_data, label_embedding_repeated])

        x = Dense(64)(Flatten()(merged_input))
        x = LeakyReLU(alpha=0.2)(x)
        x = Dense(1, activation='sigmoid')(x)

        model = Model([input_data, input_label], x)
        return model'''

    def compile_discriminator(self):
        self.discriminator.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

    def build_gan(self):
        print("building gan...")
        self.discriminator.trainable = False
        model = Sequential()

        input_noise = self.get_noise()  # Input(shape=(self.latent_dim + 2,))
        #model.add(input_noise)
        generated_data = self.generator(input_noise)

        input_label = self.get_onehot_labels()   # Input(shape=(2,))
        #model.add(input_label)
        validity = self.discriminator(generated_data, input_label)

        model.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))
        return model

    def encode_labels(self):
        label_encoder = LabelEncoder()
        self.y_train = label_encoder.fit_transform(self.y_train)

    def get_onehot_labels(self):
        onehot_encoder = OneHotEncoder(sparse_output=False)
        encoded_labels = self.y_train.reshape(len(self.y_train), 1)
        onehot_labels = onehot_encoder.fit_transform(encoded_labels)

        return onehot_labels

    def get_sampled_labels_onehot(self, batch_size=64):
        sampled_labels = np.random.randint(0, 2, (batch_size, 1))
        sampled_labels_onehot = to_categorical(sampled_labels, num_classes=2)
        return sampled_labels_onehot

    def get_noise(self, batch_size=64):
        return np.random.normal(0, 1, (batch_size, self.latent_dim + 2))

    def plotECG(self, data):
        x1 = data[:, 0]

        x2 = data[:, 1]

        plt.subplot(2, 1, 1)
        plt.plot(x1, label='Diagramm 1')
        plt.title('Diagramm 1')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(x2, label='Diagramm 2')
        plt.title('Diagramm 2')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def train(self, epochs=10, batch_size=64):
        print("training GAN...")
        half_batch = batch_size // 2

        self.compile_discriminator()
        self.discriminator.trainable = False

        for epoch in range(epochs):
            # train discriminator on real data
            idx = np.random.randint(0, self.X_train.shape[0], half_batch)
            real_labels = np.ones((half_batch, 1))

            d_loss_real = self.discriminator.train_on_batch(self.X_train[idx], real_labels)

            # create generated data with generator using noise
            noise = self.get_noise(half_batch)
            generated_data = self.generator(noise)

            # output generated data
            # print(generated_data)
            # self.plotECG(generated_data[0])

            # train disc on generated data
            fake = np.zeros((half_batch, 1))
            d_loss_fake = self.discriminator.train_on_batch(generated_data, fake)  # sampled_labels
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

            noise = np.random.normal(0, 1, (batch_size, self.latent_dim + 2))
            # sampled_labels = np.random.randint(0, 2, (batch_size, 1))
            # sampled_labels_onehot = to_categorical(sampled_labels, num_classes=2)

            # train generator to play discriminator
            valid = np.ones((batch_size, 1))
            g_loss = self.gan.train_on_batch(noise, valid)  # , sampled_labels_onehot

            print(f"Epoch {epoch}, D Loss: {d_loss}, G Loss: {g_loss}")

    def generate_samples(self, num_samples=4):
        print("generating samples...")
        example_labels = to_categorical(np.array([0, 1, 0, 1]), num_classes=2)
        example_noise = np.random.normal(0, 1, (num_samples, self.latent_dim))
        # generated_examples = self.generator.predict([example_noise, example_labels])

    def save_gan_model(self, file_name='gan.keras'):
        self.gan.save(file_name)

    def load_gan_model(self, file_name='gan.keras'):
        self.gan = keras.models.load_model(file_name)

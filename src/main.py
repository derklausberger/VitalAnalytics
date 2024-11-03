import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import customtkinter as ctk
import numpy as np

from model.data_reader import read_train_data_from_files
from model.gan import GAN
from pages.ecg_monitoring import MonitoringPage
from pages.home import HomePage
from pages.login import LoginPage
from pages.patient_info import PatientInfoPage
from model.generator import Generator

def on_closing():
    exit()


class MainApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.current_page = None
        self.title("Vital Analytics")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = (screen_width - 1500) // 2
        y_position = (screen_height - 600) // 2
        self.geometry(f'1500x600+{x_position}+{y_position}')
        self.page_container = ctk.CTkFrame(self)
        self.page_container.pack(side="top", fill="both", expand=True)

        self.pages = {
            "homepage": HomePage(self.page_container, self),
            "loginpage": LoginPage(self.page_container, self),
            "ecgmonitoring": MonitoringPage(self.page_container, self),
            "patientinfo": PatientInfoPage(self.page_container, self)
        }

        self.protocol("WM_DELETE_WINDOW", on_closing)

        self.show_page("ecgmonitoring")

    def show_page(self, page_name):
        self.destroy_previous_page()

        new_page = self.pages.get(page_name)
        if new_page:
            new_page.pack(side="top", fill="both", expand=True)
            new_page.tkraise()

            self.current_page = new_page

            print(f"The page {page_name} is displayed.")

        else:
            print(f"The page {page_name} doesn't exist.")

    def destroy_previous_page(self):
        if self.current_page:
            self.current_page.pack_forget()


def generate_samples(num_samples):
    print("generate_samples: start...")
    generator_file = "generator.keras"
    
    # X_train enthält die datensätze
    # y_train enthält die zuordnung, also "AFIB" oder "N"
    X_train, y_train = read_train_data_from_files()

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    if not os.path.exists(generator_file):
        print("generate_samples: create gan and save generator...")

        gan = GAN(X_train, y_train)
        #gan.train(epochs=1)
        gan.generator.save_to_file(generator_file)
        #samples = gan.generate_samples(num_samples=num_samples)
    else:
        print("generate_samples: create gan and laod generator...")
        
        gan = GAN(X_train, y_train)
        gan.generator = Generator.load_from_file(generator_file)
        #generator = Generator.load_from_file('generator.keras')

    #gan.fit()

    print("generate_samples: generate samples using generator...")

    fake_samples = gan.generator.generate_samples(num_samples=num_samples)

    return gan, fake_samples, X_train[:num_samples] #gan, real_samples, fake_samples

def predict_samples(gan, real_samples, fake_samples):
    # Vorhersagen des Discriminators für echte und generierte Samples
    real_predictions = gan.discriminator.model.predict(real_samples)
    fake_predictions = gan.discriminator.model.predict(fake_samples)

    # Ergebnisse anzeigen
    print("Discriminator Predictions on Real Samples:", real_predictions)
    print("Discriminator Predictions on Fake Samples:", fake_predictions)
    
def main():
    num_samples = 5

    # Samples generieren und echte Daten für Vergleich laden
    gan, fake_samples, real_samples = generate_samples(num_samples=num_samples)
    
    # Samples durch den Discriminator klassifizieren
    predict_samples(gan, real_samples, fake_samples)

    # GUI anzeigen:
    #app = MainApplication()
    #app.mainloop()

    return 0


if __name__ == '__main__':
    main()

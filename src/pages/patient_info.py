from tkinter import ttk
import tkinter as tk

import customtkinter as ctk
from src.pages.navigation_bar import NavigationBar


class PatientInfoPage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        super().__init__(parents)

        self.controller = controller
        self.main_application = parents
        self.navigation_bar = NavigationBar(self, self.main_application, self.controller)
        self.navigation_bar.pack(side="top", fill="y")

        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Patient Information", width=800, height=50, bg_color="#40c2a2", text_color="white", font=('Lucida Sans', 18, 'bold'))
        title.pack(side="top", fill="y", padx=0, pady=0)

        # Variablen zur Verfolgung der ausgewählten Geschlechter
        self.male_var = ctk.IntVar()
        self.female_var = ctk.IntVar()


        # Checkboxen erstellen
        male_checkbox = ctk.CTkCheckBox(self, text="Male", variable=self.male_var)
        female_checkbox = ctk.CTkCheckBox(self, text="Female", variable=self.female_var)

        # Checkboxen packen
        male_checkbox.pack(anchor="c", padx=10, pady=10)
        female_checkbox.pack(anchor="c", padx=10)

        # Variable zur Verfolgung der ausgewählten Option
        self.selected_option = tk.StringVar()

        # Dropdown-Menü erstellen
        options = ["Bluthochdruck", "Normalwert", "Blutniederdruck"]
        dropdown_menu = ttk.Combobox(self, textvariable=self.selected_option, values=options)
        dropdown_menu.pack(pady=20)
        dropdown_menu.set("Blutdruck wählen...")  # Standardwert

        # print_button = ctk.CTkButton(self, text="Print Selected Option", command=self.print_selected_option)
        # print_button.pack()

    def print_selected_option(self):
        selected_option = self.selected_option.get()
        print(f"Selected Option: {selected_option}")



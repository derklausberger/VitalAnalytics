from tkinter import ttk
import tkinter as tk

import customtkinter as ctk
from src.pages.navigation_bar import NavigationBar


class PatientInfoPage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        super().__init__(parents)
        self.male_var = ctk.IntVar(value=0)
        self.female_var = ctk.IntVar(value=0)
        self.controller = controller
        self.main_application = parents
        self.navigation_bar = NavigationBar(self, self.main_application, self.controller)
        self.navigation_bar.pack(side="top", fill="y")

        self.create_widgets()

    def update_checkboxes(self):
        # Überprüfe, ob Male-Checkbox ausgewählt wurde
        if self.male_var.get():
            self.female_var.set(0)  # Setze Female-Checkbox auf nicht ausgewählt

        # Überprüfe, ob Female-Checkbox ausgewählt wurde
        elif self.female_var.get():
            self.male_var.set(0)  # Setze Male-Checkbox auf nicht ausgewählt

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Patient Information", width=800, height=50, bg_color="#40c2a2", text_color="white", font=('Lucida Sans', 18, 'bold'))
        title.pack(side="top", fill="y", padx=0, pady=0)

        # Variablen zur Verfolgung der ausgewählten Geschlechter
        self.male_var = ctk.IntVar()
        self.female_var = ctk.IntVar()

        # Checkboxen erstellen
        male_checkbox = ctk.CTkCheckBox(self, text="Male", font=('Lucida Sans', 12), variable=self.male_var, width=200, command=self.update_checkboxes())
        female_checkbox = ctk.CTkCheckBox(self, text="Female", variable=self.female_var, font=('Lucida Sans', 12), command=self.update_checkboxes())

        # Checkboxen packen
        male_checkbox.pack(side="left", anchor="w", padx=10, pady=10)
        female_checkbox.pack(side="left", anchor="w", padx=10)

        self.selected_option = tk.StringVar()

        # dropdown menu
        options = ["High Blood Pressure", "Normal Blood Pressure", "Low Blood Pressure"]
        dropdown_menu = ttk.Combobox(self, textvariable=self.selected_option, values=options, font=('Lucida Sans', 12))
        dropdown_menu.pack(pady=20)
        dropdown_menu.set("Blood Pressure...")  # Standardwert

        # print_button = ctk.CTkButton(self, text="Print Selected Option", command=self.print_selected_option)
        # print_button.pack()

    def print_selected_option(self):
        selected_option = self.selected_option.get()
        print(f"Selected Option: {selected_option}")



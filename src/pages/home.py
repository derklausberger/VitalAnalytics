import customtkinter as ctk
from src.pages.navigation_bar import NavigationBar
import tkinter as tk

class HomePage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        super().__init__(parents)

        self.controller = controller
        self.main_application = parents
        self.navigation_bar = NavigationBar(self, self.main_application, self.controller)
        self.navigation_bar.pack(side="top", fill="y")

        self.create_widgets()

    def create_widgets(self):
        welcome_label = ctk.CTkLabel(self, text="Welcome to \n Vital Analytics!", font=('Lucida Sans', 25, 'bold'), text_color="#ffffff", width=1000, height=85, bg_color="#40c2a2")
        welcome_label.pack(side="top", fill="x", padx=0, pady=0)

        left_aligned_text = "Navigate to..." \
                            "\n"\
                            "\n ...Patient Information" \
                            "\n \u2022 to specify the patient's gender (male/female)" \
                            "\n \u2022 to specify if patient has blood pressure related issues" \
                            "\n" \
                            "\n ...ECG Monitoring" \
                            "\n \u2022 consumes ECG data"\
                            "\n \u2022 outputs classification (AFib or no AFib)" \
                            "\n \u2022 values can be viewed as table and line plot"\
                            "\n \u2022 resetting the values is also possible"

        description_label = tk.Label(self, text=left_aligned_text, anchor="c", justify="left", padx=10, pady=10, font=('Lucida Sans', 12))
        description_label.pack(fill="x")




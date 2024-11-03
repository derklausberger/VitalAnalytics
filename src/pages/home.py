import customtkinter as ctk
from pages.navigation_bar import NavigationBar

class HomePage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        super().__init__(parents)

        self.controller = controller
        self.main_application = parents
        self.navigation_bar = NavigationBar(self, self.main_application, self.controller)
        self.navigation_bar.pack(side="top", fill="y")

        self.create_widgets()

    def create_widgets(self):
        welcome_label = ctk.CTkLabel(self, text="Welcome to \n Vital Analytics!", font=('Lucida Sans', 25, 'bold'), text_color="#ffffff", width=800, height=85, bg_color="#40c2a2")
        welcome_label.pack(side="top", fill="y", padx=0, pady=0)

        explain_label = ctk.CTkLabel(self, text="Purpose of this application", width=800, font=('Lucida Sans', 14))
        explain_label.pack(pady=20, padx=10)

        # Unterpunkte
        subpoints_frame = ctk.CTkFrame(self)
        subpoint1_label = ctk.CTkLabel(subpoints_frame, text="- displaying ecg simulation", font=('Lucida Sans', 14))
        subpoint2_label = ctk.CTkLabel(subpoints_frame, text="- displaying atrial fibrillation in ecg", font=('Lucida Sans', 14))
        subpoint3_label = ctk.CTkLabel(subpoints_frame, text="- showing differences in diagnoses", font=('Lucida Sans', 14))

        subpoints = [subpoint1_label, subpoint2_label, subpoint3_label]

        for subpoint in subpoints:
            subpoint.pack(anchor="w")

        # Anordnen des Subpunkte-Frames
        subpoints_frame.pack(pady=20, padx=20)



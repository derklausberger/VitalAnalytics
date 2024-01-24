import customtkinter as ctk


class NavigationBar(ctk.CTkFrame):
    def __init__(self, parent, controller, main_app_instance):
        super().__init__(parent)
        self.controller = controller
        self.main_app_instance = main_app_instance
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        home_button = ctk.CTkButton(self, text="Home", fg_color="#40c2a2", hover_color="#6AA391", font=('Lucida Sans', 14), text_color="#ffffff", command=lambda: self.main_app_instance.show_page("homepage"))
        home_button.pack(side="left", fill="x", padx=10, pady=10)

        patient_info_button = ctk.CTkButton(self, text="Patient Info", fg_color="#40c2a2", hover_color="#6AA391", font=('Lucida Sans', 14), text_color="#ffffff", command=lambda: self.main_app_instance.show_page("patientinfo"))
        patient_info_button.pack(side="left", fill="x", padx=10, pady=10)

        ecg_button = ctk.CTkButton(self, text="ECG Monitoring", fg_color="#40c2a2", hover_color="#6AA391", font=('Lucida Sans', 14), text_color="#ffffff", command=lambda: self.main_app_instance.show_page("ecgmonitoring"))
        ecg_button.pack(side="left", fill="x", padx=10)

        logout_button = ctk.CTkButton(self, text="Logout", fg_color="#be383b", hover_color="#9D2E31", font=('Lucida Sans', 14), text_color="#ffffff", command=lambda: self.main_app_instance.show_page("loginpage"))
        logout_button.pack(side="left", fill="x", padx=10)

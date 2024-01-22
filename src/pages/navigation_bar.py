import customtkinter as ctk


class NavigationBar(ctk.CTkFrame):
    def __init__(self, parent, controller, main_app_instance):
        super().__init__(parent)
        self.controller = controller
        self.main_app_instance = main_app_instance
        self.create_navigation_buttons()

    def create_navigation_buttons(self):
        print("navbuttons sollten erstellt werden")
        # Home Button
        home_button = ctk.CTkButton(self, text="Home", command=lambda: self.main_app_instance.show_page("homepage"))
        home_button.pack(side="top", fill="x", pady=5)
        print("homebutton ist okay")

        # ECG Monitoring Button
        ecg_button = ctk.CTkButton(self, text="ECG Monitoring", command=lambda: self.main_app_instance.show_page("ecgmonitoring"))
        ecg_button.pack(side="top", fill="x", pady=5)
        print("lellllllllllll")

        # Logout Button
        logout_button = ctk.CTkButton(self, text="Logout", command=lambda: self.main_app_instance.show_page("loginpage"))
        logout_button.pack(side="top", fill="x", pady=5)
        print("lol")

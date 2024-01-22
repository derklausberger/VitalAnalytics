import customtkinter as ctk
from src.pages.navigation_bar import NavigationBar


class HomePage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        super().__init__(parents)
        # self.container = ctk.CTkFrame

        self.controller = controller
        self.main_application = parents
        self.navigation_bar = NavigationBar(self, self.main_application, self.controller)
        self.navigation_bar.pack(side="left", fill="y")

        self.create_widgets()
        # self.container.pack()

    def create_widgets(self):
        welcome_label = ctk.CTkLabel(self, text="Welcome to Vital Analytics!", width=720)
        welcome_label.pack(pady=20, padx=20)


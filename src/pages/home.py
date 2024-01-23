import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        ctk.CTkFrame.__init__(self, parents)
        # self.container = ctk.CTkFrame

        self.controller = controller
        self.main_application = parents
        self.create_widgets()
        # self.container.pack()

    def create_widgets(self):
        welcome_label = ctk.CTkLabel(self, text="Welcome to Vital Analytics!")
        welcome_label.pack(pady=20)

        logout_button = ctk.CTkButton(self, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

    def logout(self):
        self.controller.show_page("loginpage")

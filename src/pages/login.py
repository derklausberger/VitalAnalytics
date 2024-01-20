import customtkinter as ctk
from src.utils.authentication import check_login


class LoginPage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        ctk.CTkFrame.__init__(self, parents)
        # self.container = ctk.CTkFrame
        self.password_entry = None
        self.username_entry = None
        self.controller = controller
        self.main_application = parents

        self.login_window()
        # self.container.pack(self)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if check_login(username, password):
            self.controller.show_page("ecgmonitoring")
        else:
            print("Login failed!")

    def login_window(self):
        label = ctk.CTkLabel(master=self, text="Vital Analytics")
        label.pack(pady=12, padx=10)

        username_input = ctk.CTkEntry(master=self, placeholder_text="Username")
        username_input.pack(pady=12, padx=10)
        self.username_entry = username_input

        password_input = ctk.CTkEntry(master=self, placeholder_text="Password", show="*")
        password_input.pack(pady=12, padx=10)
        self.password_entry = password_input

        button = ctk.CTkButton(master=self, text="Login", command=self.login)
        button.pack(pady=12, padx=10)

        checkbox = ctk.CTkCheckBox(master=self, text="Remember Me")
        checkbox.pack(pady=12, padx=10)





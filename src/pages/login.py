import customtkinter as ctk
from src.utils.authentication import check_login


class LoginPage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        ctk.CTkFrame.__init__(self, parents)
        self.password_entry = None
        self.username_entry = None
        self.controller = controller
        self.main_application = parents

        self.login_window()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if check_login(username, password):
            self.controller.show_page("ecgmonitoring")
        else:
            print("Login failed!")

    def login_window(self):
        label = ctk.CTkLabel(master=self, text="Vital Analytics", text_color="#ffffff", width=500, height=50, bg_color="#40c2a2", font=('Lucida Sans', 22, 'bold'))
        label.pack(pady=0, padx=0)

        username_input = ctk.CTkEntry(master=self, placeholder_text="Username", font=('Lucida Sans', 16), width=200, height=40)
        username_input.pack(pady=20, padx=10)
        self.username_entry = username_input

        password_input = ctk.CTkEntry(master=self, placeholder_text="Password", show="*", font=('Lucida Sans', 16), width=200, height=40)
        password_input.pack(pady=0, padx=10)
        self.password_entry = password_input

        button = ctk.CTkButton(master=self, text="Login", fg_color="#40c2a2", hover_color="#6AA391", font=('Lucida Sans', 16, 'bold'), text_color="#ffffff", width=200, height=40, command=self.login)
        button.pack(pady=20, padx=10)

        # checkbox = ctk.CTkCheckBox(master=self, text="Remember Me")
        # checkbox.pack(pady=12, padx=10)





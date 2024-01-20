import tkinter

import customtkinter as ctk

from src.pages.ecg_monitoring import MonitoringPage
from src.pages.login import LoginPage
from src.pages.home import HomePage


class MainApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.current_page = None
        self.title("Vital Analytics")
        self.geometry("800x600")

        self.page_container = ctk.CTkFrame(self)
        self.page_container.pack(side="top", fill="both", expand=True)

        self.pages = {
            "homepage": HomePage(self.page_container, self),
            "loginpage": LoginPage(self.page_container, self),
            "ecgmonitoring": MonitoringPage(self.page_container, self)
        }

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.show_page("loginpage")

    def on_closing(self):
        exit()

    def show_page(self, page_name):
        self.destroy_previous_page()

        new_page = self.pages.get(page_name)
        if new_page:
            new_page.pack()
            new_page.tkraise()

            self.current_page = new_page

            print(f"Die Seite {page_name} wird angezeigt.")

        else:
            print(f"Die Seite {page_name} existiert nicht.")

    def destroy_previous_page(self):
        if self.current_page:
            self.current_page.pack_forget()

def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()

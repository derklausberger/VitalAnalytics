import tkinter
from tkinter import messagebox

import customtkinter as ctk

from src.pages.ecg_monitoring import MonitoringPage
from src.pages.login import LoginPage
from src.pages.home import HomePage
from src.pages.patient_info import PatientInfoPage


class MainApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.current_page = None
        self.title("Vital Analytics")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = (screen_width - 800) // 2
        y_position = (screen_height - 1020) // 2
        self.geometry(f'800x950+{x_position}+{y_position}')
        self.page_container = ctk.CTkFrame(self)
        self.page_container.pack(side="top", fill="both", expand=True)

        self.pages = {
            "homepage": HomePage(self.page_container, self),
            "loginpage": LoginPage(self.page_container, self),
            "ecgmonitoring": MonitoringPage(self.page_container, self),
            "patientinfo": PatientInfoPage(self.page_container, self)
        }

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.show_page("ecgmonitoring")

    def on_closing(self):
        exit()

    def show_page(self, page_name):
        self.destroy_previous_page()

        new_page = self.pages.get(page_name)
        if new_page:
            new_page.pack()
            new_page.tkraise()

            self.current_page = new_page

            print(f"The page {page_name} is displayed.")

        else:
            print(f"The page {page_name} doesn't exist.")

    def destroy_previous_page(self):
        if self.current_page:
            self.current_page.pack_forget()


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()

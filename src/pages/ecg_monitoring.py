import customtkinter as ctk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import src.pages.home


class MonitoringPage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        ctk.CTkFrame.__init__(self, parents)
        # self.container = ctk.CTkFrame

        self.controller = controller
        self.main_application = parents

        self.load_widgets()
        # self.container.pack(self)

    def generate(self):
        duration = 10  # time in seconds
        sampling_rate = 600  # ekg in hertz

        p_dur = 100  # p wave duration in milliseconds: 60-100
        pq_dur = 100
        qrs_dur = 100
        st_dur = 100
        t_dur = 200

        # time stamps for specific complexes
        t_p = np.linspace(0, 0.15, p_dur, endpoint=False)
        t_pq = np.linspace(0.15, 0.3, pq_dur, endpoint=False)
        t_qrs = np.linspace(0.3, 0.6, qrs_dur, endpoint=False)
        t_st = np.linspace(0.6, 0.75, st_dur, endpoint=False)
        t_t = np.linspace(0.75, 1, t_dur, endpoint=False)

        p_wave = 0.3 * np.sin(4 * np.pi * t_p)  # 0.1-0.3 mV

        pq_dist = 0 * t_pq

        # S(0.) < Q(-0.1--0.3mV) < R(1-3mV)
        qrs_complex = np.concatenate((
            (t_qrs[0:25] - t_qrs[0]) * -5,  # because last value = 0.06*5 = 0.3 = max value
            (t_qrs[25:50] - t_qrs[25]) * 55 - (t_qrs[24] - t_qrs[0]) * 5,  #
            (t_qrs[50:75] - t_qrs[50]) * -57 + (t_qrs[49] - t_qrs[25]) * 50,
            (t_qrs[75:100] - t_qrs[75]) * 7 - (t_qrs[74] - t_qrs[50]) * 7
        ))

        st_dist = 0 * t_st

        t_wave = - 0.6 * np.sin(4 * np.pi * t_t)

        ekg_data = np.concatenate((p_wave, pq_dist, qrs_complex, st_dist, t_wave))

        t = np.concatenate((t_p, t_pq, t_qrs, t_st, t_t))
        np.savetxt('ekg.csv', np.column_stack((t, ekg_data)), delimiter=',', header='Time,EKG Amplitude', comments='')

    def plot(self):
        ekg_df = pd.read_csv('ekg.csv')

        fig, ax = plt.subplots()

        ax.plot(ekg_df['Time'], ekg_df['EKG Amplitude'])
        ax.set_xlabel('time(s)')
        ax.set_ylabel('amplitude')
        ax.set_title('data')
        ax.grid(True)
        ax.set_xlim(0, 10)
        ax.set_ylim(-2, 5)
        return fig

    def load_widgets(self):
        ctk.set_appearance_mode("light")

        ctk.set_default_color_theme("green")

        logout_button = ctk.CTkButton(master=self, text="Logout", command=self.logout)
        logout_button.pack(pady=50, padx=20)

        label = ctk.CTkLabel(self, text="ECG Monitoring")
        label.pack(pady=50, padx=20)

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        canvas = FigureCanvasTkAgg(self.plot(), master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

    def logout(self):
        self.controller.show_page("loginpage")

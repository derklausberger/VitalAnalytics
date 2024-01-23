import customtkinter as ctk
import mplcursors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.pages.navigation_bar import NavigationBar

class MonitoringPage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        super().__init__(parents)
        self.controller = controller
        self.main_application = parents
        self.navigation_bar = NavigationBar(self, self.main_application, self.controller)
        self.navigation_bar.pack(side="top", fill="y")

        self.load_widgets()

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
        try:
            ekg_df = pd.read_csv('ekg.csv')
        except FileNotFoundError:
            print("MonitoringPage.plot: File 'ekg.csv' not found. Returning an empty figure.")
            return plt.figure()

        fig, ax = plt.subplots()

        line, = ax.plot(ekg_df['Time'], ekg_df['EKG Amplitude'])
        ax.set_xlabel('time(s)')
        ax.set_ylabel('amplitude')
        ax.set_title('EKG-Plot')
        ax.grid(True)
        ax.set_xlim(0, 10)
        ax.set_ylim(-2, 5)

        def label_text(self):
            index = int(self.index)
            return f'Zeit: {ekg_df["Time"].iloc[index]:.2f}s\nAmplitude: {ekg_df["EKG Amplitude"].iloc[index]:.2f}'

        # Aktivieren von mplcursors für den Line Plot
        cursor = mplcursors.cursor(line, hover=True)
        cursor.connect('add', lambda self: self.annotation.set_text(label_text(self)))
        return fig

    def load_widgets(self):
        label = ctk.CTkLabel(self, text="ECG Monitoring", height=50, bg_color="#40c2a2", text_color="white", font=('Lucida Sans', 18, 'bold'), width=800)
        label.pack(pady=0, padx=0)

        reset_button = ctk.CTkButton(self, text="RESET", width=100, fg_color="#be383b", hover_color="#9D2E31", font=('Lucida Sans', 14), text_color="#ffffff")
        reset_button.pack(side="top", padx=10, pady=10)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True)

        canvas = ctk.CTkCanvas(table_frame, width=600, bg="#40c2a2")
        canvas.pack(side="left", padx=20, pady=20, expand=True)

        scrollbar = ctk.CTkScrollbar(table_frame, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        table_entries_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=table_entries_frame, anchor="nw")

        table_entries_list = self.table(table_entries_frame)

        for i, row_entries in enumerate(table_entries_list):
            for j, table_entry in enumerate(row_entries):
                table_entry.grid(row=i, column=j)

        canvas.configure(yscrollcommand=scrollbar.set)
        table_entries_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        plot_frame = ctk.CTkFrame(self)
        plot_frame.pack(pady=20, padx=60, fill="both", expand=False)

        plot_canvas = FigureCanvasTkAgg(self.plot(), master=plot_frame)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack(side="left", fill="both", expand=False)

    def table(self, parent_frame):
        lst = [('Time(s)', 'ECG Amplitude', 'P-Wave', 'QRS-Complex', 'T-Wave', 'HF'),
               (2, 'Aaryan', 'Pune', 18, 'iwas', 'iwas'),
               (3, 'Vaishnavi', 'Mumbai', 20, 'iwas', 'iwas'),
               (4, 'Rachna', 'Mumbai', 21, 'iwas', 'iwas'),
               (5, 'Shubham', 'Delhi', 21, 'iwas', 'iwas'),
               (1, 'Raj', 'Mumbai', 19, 'iwas', 'iwas'),
               (2, 'Aaryan', 'Pune', 18, 'iwas', 'iwas'),
               (3, 'Vaishnavi', 'Mumbai', 20, 'iwas', 'iwas'),
               (4, 'Rachna', 'Mumbai', 21, 'iwas', 'iwas'),
               (5, 'Shubham', 'Delhi', 21, 'iwas', 'iwas'),
               (1, 'Raj', 'Mumbai', 19, 'iwas', 'iwas'),
               (2, 'Aaryan', 'Pune', 18, 'iwas', 'iwas'),
               (3, 'Vaishnavi', 'Mumbai', 20, 'iwas', 'iwas'),
               (4, 'Rachna', 'Mumbai', 21, 'iwas', 'iwas'),
               (5, 'Shubham', 'Delhi', 21, 'iwas', 'iwas')]

        total_rows = len(lst)
        total_columns = len(lst[0])

        table_entries = []

        for i in range(total_rows):
            row_entries = []
            for j in range(total_columns):
                table_entry = ctk.CTkEntry(parent_frame, width=100)
                table_entry.grid(row=i, column=j)
                table_entry.insert(0, lst[i][j])
                row_entries.append(table_entry)
            table_entries.append(row_entries)

        return table_entries

import threading
import time
import customtkinter as ctk
import mplcursors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pages.navigation_bar import NavigationBar


class MonitoringPage(ctk.CTkFrame):
    def __init__(self, parents, controller):
        super().__init__(parents)
        self.animation_thread = None
        self.controller = controller
        self.main_application = parents
        self.navigation_bar = NavigationBar(self, self.main_application, self.controller)
        self.navigation_bar.pack(side="top", fill="x")

        # todo: refactor the following ([0] ist nicht schön & übergeben wäre netter als in da gui generieren
        #  oder sogar generieren währen gui schon da is inkl. lade animation)
        self.data = np.random.rand(650000, 2)
        #self.data = generate_samples_for_plotting()[0]

        self.window_size = 100  # Anzahl der Punkte, die gleichzeitig angezeigt werden
        self.start_idx = 0
        self.zoom_factor = 1.1
        self.min_window_size = 50  # Minimaler Zoom-Faktor (maximaler Zoom)
        self.fig, self.ax = plt.subplots(2, 1, figsize=(10, 6))

        self.load_widgets()

    def load_widgets(self):
        # header und reset button
        label = ctk.CTkLabel(self, text="ECG Monitoring", height=50, bg_color="#40c2a2", text_color="white",
                             font=('Lucida Sans', 18, 'bold'))
        label.pack(side="top", fill="x", pady=0, padx=0)

        reset_button = ctk.CTkButton(self, text="RESET", width=100, fg_color="#be383b", hover_color="#9D2E31",
                                     font=('Lucida Sans', 14), text_color="#ffffff")
        reset_button.pack(side="top", padx=10, pady=10)

        # plot frame
        plot_frame = ctk.CTkFrame(self)
        plot_frame.pack(side="left", fill="both", expand=False)

        self.plot_ecg()

        plot_canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        plot_canvas.draw()
        plot_canvas.get_tk_widget().pack(side="top", fill="both", expand=False)

        # zoom buttons
        button_frame = ctk.CTkFrame(plot_frame)
        button_frame.pack(side="top", pady=10)

        zoom_in_button = ctk.CTkButton(button_frame, text="Zoom In", command=lambda: self.zoom(1 / self.zoom_factor))
        zoom_out_button = ctk.CTkButton(button_frame, text="Zoom Out", command=lambda: self.zoom(self.zoom_factor))
        zoom_in_button.pack(side="left", padx=5)
        zoom_out_button.pack(side="left", padx=5)
        
        #table_frame
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(side="right", fill="both", expand=True)

        canvas = ctk.CTkCanvas(table_frame, bg="#40c2a2")
        canvas.pack(side="left", fill="both", padx=20, pady=20, expand=True)

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

    def start_animation(self, ani):
        #def run_animation():
        ani.event_source.start()
        plt.show()

        #self.tk.after(0, run_animation)
    
    
    def plot_ecg(self):
        data = self.data
        data_plot1 = data[:, 0]
        data_plot2 = data[:, 1]

        # Initialer Plot
        self.line1, = self.ax[0].plot(data_plot1[:self.window_size], label="MLII")
        self.ax[0].set_ylabel("MLII/mV")
        self.ax[0].set_xlim(0, self.window_size)
        
        self.line2, = self.ax[1].plot(data_plot2[:self.window_size], label="V5")
        self.ax[1].set_ylabel("V5/mV")
        #self.ax[1].set_xlabel("time/seconds")
        self.ax[1].set_xlim(0, self.window_size)

        self.fig.text(0.5, 0.95, "Time/Seconds", ha='center', va='center', fontsize=12)

        self.fig.set_size_inches(8, 4)

        # Slider für horizontales Scrollen
        ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.slider = Slider(ax_slider, 'Scroll', 0, len(data_plot1) - self.window_size, valinit=0)
        self.slider.on_changed(self.update_plot)

        # Event für das Mausrad (Zoom-Funktion)
        self.fig.canvas.mpl_connect('scroll_event', self.zoom)

        # mplcursors für Interaktivität
        self.add_cursor(self.ax[0], data_plot1, "MLII")
        self.add_cursor(self.ax[1], data_plot2, "V5")

        #plt.tight_layout()
        #plt.show()

    def update_plot(self, val):
        # Hole den Startindex aus dem Slider
        self.start_idx = int(self.slider.val)
        
        # Berechne den Endindex
        end_idx = min(self.start_idx + self.window_size, len(self.data))

        # Überprüfe, ob der Startindex gültig ist
        if self.start_idx < len(self.data):
            # Aktualisiere den Plot
            x_data0 = np.arange(self.window_size)
            y_data0 = self.data[self.start_idx:end_idx, 0]
            self.line1.set_data(x_data0, y_data0)

            x_data1 = np.arange(self.window_size)
            y_data1 = self.data[self.start_idx:end_idx, 1]
            self.line2.set_data(x_data1, y_data1)

            #self.line1.set_ydata(self.data[self.start_idx:end_idx, 0])  # MLII
            #self.line2.set_ydata(self.data[self.start_idx:end_idx, 1])  # V5

            # Setze die x-Achse
            self.ax[0].set_xlim(0, end_idx - self.start_idx)
            self.ax[1].set_xlim(0, end_idx - self.start_idx)

            # x-achsen beschriftung aktualisieren
            num_ticks = 6
            tick_positions = np.linspace(0, end_idx - self.start_idx, num_ticks).astype(int)  # Angepasste Tick-Positionen
            tick_labels = [str(self.start_idx + pos) for pos in tick_positions]

            # Update der x-Achsen-Labels
            self.ax[0].set_xticks(tick_positions)
            self.ax[0].set_xticklabels(tick_labels)
            self.ax[1].set_xticks(tick_positions)
            self.ax[1].set_xticklabels(tick_labels)


            # Zeichne das Diagramm neu
            self.fig.canvas.draw_idle()


    def zoom(self, factor):
        # Berechne die neue Fenstergröße
        new_window_size = int(self.window_size * factor)
        if new_window_size < self.min_window_size:
            new_window_size = self.min_window_size
        if new_window_size > len(self.data):
            new_window_size = len(self.data)

        self.window_size = new_window_size
        self.slider.valmax = len(self.data) - self.window_size

        #self.fig.canvas.draw_idle()
        self.update_plot(self.slider.val)

    # cursor für die legende
    def add_cursor(self, ax, data, label):
        cursor = mplcursors.cursor(ax, hover=True)

        def update_annotation(sel):
            index = int(sel.target.index)
            
            if 0 <= index < len(data):
                sel.annotation.set_text(
                    f"Time: {index / 360:.2f}s\n{label}: {data[index]:.2f}"
                )
            else:
                sel.annotation.set_text("Index außerhalb der Daten")

        cursor.connect("add", update_annotation)
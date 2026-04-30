from math import sqrt
import tkinter as tk
from tkinter import DISABLED, ttk
import numpy as np
import matplotlib.pyplot as plt
import csv
import random
import json
from idlelib.tooltip import Hovertip
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DynamicSignalGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Multi-Wave Generator")
        self.root.geometry("1700x1500")
        self.root.state('zoomed')
        
        self.waves = [] 

        self.rms_values = []

        self.create_ui()
        
        self.add_wave() 
        # Call to destroy the physical window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        plt.close('all')    
        self.root.quit()    
        self.root.destroy() # Destroy the physical window
       
    def create_ui(self):
        # --- Left Panel: Controls ---
        self.left_panel = ttk.Frame(self.root)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Header with the "+" Button
        header_frame = ttk.Frame(self.left_panel)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header_frame, text="Wave Controls", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # The '+ Add Wave' button
        add_btn = ttk.Button(header_frame, text="+", command=self.add_wave)
        add_btn.pack(side=tk.RIGHT)

        # The '- Remove Wave' button
        rem_btn = ttk.Button(header_frame, text="-", command=self.remove_wave)
        rem_btn.pack(side=tk.RIGHT)

        # A frame to hold all the dynamically added wave controls
        self.waves_frame = ttk.Frame(self.left_panel)
        self.waves_frame.pack(fill=tk.BOTH, expand=True)

        #The Right Panel:
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.top_info_frame = ttk.Frame(self.plot_frame)
        self.top_info_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        self.total_rms_var = tk.StringVar(value="RMS: 0.000")
        rms_label = ttk.Label(self.top_info_frame, textvariable=self.total_rms_var, font=("Arial", 14, "bold"), foreground="red")
        rms_label.pack(side=tk.RIGHT, padx=20)

        self.bottom_control_frame = ttk.Frame(self.plot_frame)
        self.bottom_control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        ttk.Label(self.bottom_control_frame, text="Sampling frequency:").pack(side=tk.LEFT, padx=(20, 2))
        self.fs_var = tk.DoubleVar(value=10.0)
        self.fs_var.trace_add("write", lambda *args: self.update_plot())
        cycles_box_fs = ttk.Spinbox(self.bottom_control_frame, from_=0.1, to=50000.0, increment=1.0, textvariable=self.fs_var, width=6, command=self.update_plot)
        cycles_box_fs.pack(side=tk.LEFT)
        cycles_box_fs.bind("<Return>", self.update_plot)

        self.is_discrete = tk.BooleanVar(value=False)
        toggle_btn = ttk.Checkbutton(self.bottom_control_frame, text="Discrete (Dots) View", variable=self.is_discrete, command=self.update_plot)
        toggle_btn.pack(side=tk.LEFT, padx=30)
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=100)
        self.ax.set_title("Signals")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        self.line, = self.ax.plot(100, np.zeros_like(100), color='red', linewidth=2)
        
        # Set a wider Y-axis since we are adding multiple waves together
        self.ax.set_ylim(-20, 20) 

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # The 'Export' button
        exp_btn = ttk.Button(self.left_panel, text="Export", command=self.Export_JSON)
        exp_btn.pack(side=tk.RIGHT)

    def add_wave(self):
        """Creates a new set of controls and adds them to the list."""
        wave_id = len(self.waves) + 1

        # 1. Create variables for this specific wave
        w_type = tk.StringVar(value="Sine")
        w_noise = tk.DoubleVar(value=0.0)
        
        # 2. Create a frame
        frame = ttk.LabelFrame(self.waves_frame, text=f"Wave {wave_id}", padding=(10, 15))
        frame.pack(fill=tk.X, pady=5)

        # 3. Add the Dropdown
        waveforms = ["Sine", "Square", "Triangle", "Positive Sine", "Peak"]
        dropdown = ttk.Combobox(frame, textvariable=w_type, values=waveforms, state="readonly", width=10)
        dropdown.grid(row=0, column=0, padx=5, pady=5)
        dropdown.bind("<<ComboboxSelected>>", self.update_plot)

        # 4. Add Frequency
        ttk.Label(frame, text="Freq: ").grid(row=0, column=1)
        w_freq = tk.DoubleVar(value=1.0)
        w_freq.trace_add("write", lambda *args: self.update_plot())
        freq_entry = ttk.Spinbox(frame, from_=0.0, to=50000.0, increment=0.1, textvariable=w_freq, width=6, command=self.update_plot)
        #freq_slider= ttk.Scale(frame, from_=1, to=50, variable=w_freq, command=self.update_plot, cursor="hand2")
        freq_entry.grid(row=0, column=2, padx=5)
        freq_entry.delete(0,tk.END)
        freq_entry.insert(0,"0.0")
        # Hovertip(freq_slider, str(w_freq.get()), hover_delay=5)

        # 5. Add Amplitude
        ttk.Label(frame, text="Amp: ").grid(row=0, column=3)
        w_amp = tk.DoubleVar(value=1.0)
        w_amp.trace_add("write", lambda *args: self.update_plot())
        amp_entry = ttk.Spinbox(frame, from_=0.1, to=500.0, increment=0.1, textvariable=w_amp, width=6, command=self.update_plot)
        amp_entry.grid(row=0, column=4, padx=5)
        amp_entry.delete(0,tk.END)
        amp_entry.insert(0,"0.0")
        # Hovertip(amp_slider, str(w_amp.get()), hover_delay=5)

        # 6. Add Noise Slider
        ttk.Label(frame, text="Noise: ").grid(row=0, column=5)
        noise_slider = ttk.Scale(frame, from_=0.1, to=100.0, variable=w_noise, length=80, command=self.update_plot, cursor="hand2")
        noise_slider.grid(row=0, column=6, padx=5)
        Hovertip(noise_slider, str(w_noise.get()), hover_delay=5)

        # 7. Add start_time
        ttk.Label(frame, text="Start time (ms): ").grid(row=0, column=7)
        w_s_time = tk.DoubleVar(value=0.0)
        w_s_time.trace_add("write", lambda *args: self.update_plot())
        s_time_entry = ttk.Spinbox(frame, from_=0, to=50000, increment=1, textvariable=w_s_time, width=6, command=self.update_plot)
        s_time_entry.grid(row=0, column=8, padx=5)
        s_time_entry.delete(0,tk.END)
        s_time_entry.insert(0,"0.0")

        # 8. Add duration
        ttk.Label(frame, text="Duration (ms): ").grid(row=0, column=9)
        w_duration = tk.DoubleVar(value=1.0)
        w_duration.trace_add("write", lambda *args: self.update_plot())
        duration_entry = ttk.Spinbox(frame, from_=0, to=50000, increment=1, textvariable=w_duration, width=6, command=self.update_plot)
        duration_entry.grid(row=0, column=10, padx=5)
        duration_entry.delete(0,tk.END)
        duration_entry.insert(0,"0.0")

        # 9. Add RMS
        ttk.Label(frame, text="RMS: ").grid(row=0, column=11)
        rms_display = tk.StringVar(value="0.00")
        ttk.Entry(frame, textvariable=rms_display, width=6, state=tk.DISABLED).grid(row=0, column=12, padx=5)

        # 10. Store everything in our list so the math function can find it
        self.waves.append({
            "frame": frame,
            "type": w_type,
            "freq": w_freq,
            "amp": w_amp,
            "noise": noise_slider,
            "rms_display": rms_display,
            "start_time": w_s_time,
            "duration": w_duration
        })
        rms = 0
        self.rms_values.append(0.0)
        # Update the plot to reflect the new wave
        self.update_plot()

    def remove_wave(self):
        if(len(self.waves)>0):
            wave_id = len(self.waves) - 1

            last_wave = self.waves.pop()

            last_wave["frame"].destroy()

            self.rms_values.pop()
            
            self.update_plot()

    
    def Export_JSON(self):
        filename = "SignalData.json"
       
        data = self.generate_merged_signal()
        if (len(data)<=0):
            rms_final =0.0
        else:
            rms_final = np.sqrt(np.mean(data*data))
        export_dict = {
            "f_sample": self.fs_var.get(),
            "rms_signal": str(rms_final),
            "data": data.tolist()
        }

        # 4. Write it to a file
        with open(filename, "w") as json_file:
            # indent=4 makes the file highly readable to human eyes!
            json.dump(export_dict, json_file, indent=4)
            
        print(f"Successfully exported data to {filename}!")

    def generate_merged_signal(self):
        max_time = 0.0
        try:
            fs = float(self.fs_var.get())
        except tk.TclError:
            fs = 0.0
        for wave in self.waves:
            try:
                st = wave["start_time"].get() / 1000
            except tk.TclError:
                st = 0.0
            try:
                duration = wave["duration"].get() / 1000
            except tk.TclError:
                duration = 0.0
            if(max_time<st+duration):
                max_time = st + duration

        try:
            time = np.linspace(0, max_time, int(max_time * fs))
        except tk.TclError:
            time = np.linspace(0, max_time, int(max_time * 0))
        merged_wave = np.zeros_like(time)
        # Loop through every wave the user has added
        i = 0
        for wave in self.waves:
            w_type = wave["type"].get()
            f = 0.0
            a = 0.0
            try:
                st = wave["start_time"].get() / 1000
            except tk.TclError:
                st = 0.0
            try:
                duration = wave["duration"].get() / 1000
            except tk.TclError:
                duration = 0.0

            try:
                f = float(wave["freq"].get())
            except tk.TclError:
                f = 0.0
            try:
                a = float(wave["amp"].get())
            except tk.TclError:
                a = 0.0
            n = wave["noise"].get()

            t = np.linspace(st, st+duration, int(duration * fs))

            # Generate the math for this specific wave
            if w_type == "Sine":
                y = a * np.sin(2 * np.pi * f * t)
            elif w_type == "Square":
                y = a * np.sign(np.sin(2 * np.pi * f * t))
            elif w_type == "Triangle":
                y = a * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * f * t))
            elif w_type == "Positive Sine":
                y = abs(a * np.sin(2 * np.pi * f * t))
            elif w_type == "Peak":
                y = a - abs(a * np.sin(2 * np.pi * f * t))
            else:
                y = np.zeros_like(t)
            if(st>0):
                st_srs = np.linspace(0, st, int(st* fs))
                st_zeros = np.zeros_like(st_srs)
                y = np.concatenate((st_zeros, y))
            if(st+duration)<max_time:
                end_srs = np.linspace(st+duration, max_time, int((max_time - (st+duration)) * fs))
                end_zeros = np.zeros_like(end_srs)
                print(len(end_zeros))
                y = np.concatenate((y, end_zeros))
            noise_amplitude = n / 100.0
            noise_array = np.random.uniform(-noise_amplitude, noise_amplitude, size=len(time))
            y = y + noise_array

            # Generate a RMS
            if (len(y)<=0):
                rms =0.0
            else:
                rms = np.sqrt(np.mean(y*y))
            self.rms_values[i] = rms
            wave["rms_display"].set(f"{rms:.3f}")
            i = i+1
            # ADD it to the total merged wave (Superposition)
            merged_wave += y
        
        rms_final = np.sqrt(np.mean(merged_wave*merged_wave))
        self.total_rms_var.set(f"RMS: {rms_final:.3f}")

        return merged_wave

    def update_plot(self, event=None):
        """Updates the graph with the new merged data."""
        max_time = 0.0
        try:
            fs = float(self.fs_var.get())
        except tk.TclError:
            fs = 0.0
        for wave in self.waves:
            try:
                st = wave["start_time"].get() / 1000
            except tk.TclError:
                st = 0.0
            try:
                duration = wave["duration"].get() / 1000
            except tk.TclError:
                duration = 0.0
            if(max_time<st+duration):
                max_time = st + duration
        t = np.linspace(0, max_time, int(max_time * fs))
        y_data = self.generate_merged_signal()

        self.ax.clear()
        self.ax.set_title("Signals")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)

        if self.is_discrete.get():
            self.ax.plot(t, y_data, color='red', marker='o', markersize=3, linestyle='none')
        else:
            self.ax.plot(t, y_data, color='red')
        self.canvas.draw_idle()

if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicSignalGeneratorApp(root)
    root.mainloop()
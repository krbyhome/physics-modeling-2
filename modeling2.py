import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

splits_number = 2
split_width = 0.001
period = 0.005
wave_length = 400e-9
end_angle = 0.01
step_count = 10000
max_wave_length = 500e-9

def intensive(splits_number, split_width, period, wave_length, rad):
    alpha = (np.pi * split_width * np.sin(rad)) / wave_length
    beta = (np.pi * period * np.sin(rad)) / wave_length
    return (np.sin(splits_number * beta) / np.sin(beta)) ** 2 * (np.sin(alpha) / alpha) ** 2

def count_graph_data(splits_number, split_width, period, wave_length, end_angle, step_count):
    step = end_angle * 2 / step_count
    intensive_data = []
    angle_data = []

    for rad in np.arange(-end_angle, end_angle + step, step):
        intensive_data.append(intensive(splits_number, split_width, period, wave_length, rad))
        angle_data.append(rad)

    return np.array(intensive_data), np.array(angle_data)

def wave_length_to_rgb(wavelength, gamma):
    wave_len = wavelength / 1e-9
    if 380 <= wave_len <= 440:
        return 0.5 * gamma, 0, 0.5 * gamma
    elif 440 <= wave_len <= 490:
        return 0, 0, 1.0
    elif 490 <= wave_len <= 510:
        return 0.0, gamma, gamma
    elif 510 <= wave_len <= 580:
        return 0, gamma, 0.0
    elif 580 <= wave_len <= 645:
           return gamma, 0.5 * gamma, 0
    elif 645 <= wave_len <= 770:
        return gamma, 0.0, 0.0
    else:
        return gamma, gamma, gamma

def draw_lines(intensive_data, angle_data, wave_length, end_angle, intensive_data_2 = 0, angle_data_2 = 0):
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    ax.cla()

    min_x = -end_angle
    max_x = end_angle
    max_intensity = np.max(intensive_data)
    # max_intensity2 = np.max(intensive_data_2)

    for i in range(len(intensive_data)):
        normalized_x = (angle_data[i] - min_x) / (max_x - min_x)
        line_x = normalized_x * canvas.get_tk_widget().winfo_width()
        color = wave_length_to_rgb(wave_length, abs(intensive_data[i] / max_intensity))

        # normalized_x_2 = (angle_data_2[i] - min_x) / (max_x - min_x)
        # line_x_2 = normalized_x_2 * canvas.get_tk_widget().winfo_width()
        # color_2 = wave_length_to_rgb(max_wave_length, abs(intensive_data_2[i] / max_intensity2))

        # if intensive_data_2[i] > intensive_data[i]:
        #     ax.plot([line_x_2, line_x_2], [0, canvas.get_tk_widget().winfo_height()], color=color_2, linewidth=0.1)
        #     continue

        ax.plot([line_x, line_x], [0, canvas.get_tk_widget().winfo_height()], color=color, linewidth=0.1)

    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def draw_graph(intensive_data, angle_data, intensive_data_2 = 0, angle_data_2 = 0):
    fig, ax = plt.subplots()
    ax.plot(angle_data, intensive_data, color='blue')
    ax.plot(angle_data_2, intensive_data_2, color='orange')
    ax.set_xlabel('Angle Θ, rad')
    ax.set_ylabel('Intensity I/I₀, W/m²')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def on_submit():
    splits_number = int(entries["Количество разбиений"].get())
    split_width = float(entries["Ширина разбиений"].get())
    period = float(entries["Период"].get())
    wave_length = float(entries["Длина волны"].get())
    end_angle = float(entries["Конечный угол"].get())
    step_count = int(entries["Количество шагов"].get())
    
    if (split_width > period): 
        return

    intensive_data, angle_data = count_graph_data(
        splits_number,
        split_width,
        period,
        wave_length,
        end_angle,
        step_count
    )

    # intensive_data_2, angle_data_2 = count_graph_data(
    #     splits_number,
    #     split_width,
    #     period,
    #     max_wave_length,
    #     end_angle,
    #     step_count
    # )

    draw_graph(intensive_data, angle_data)
    draw_lines(intensive_data, angle_data, wave_length, end_angle)

    #Вызов для спектра
    # draw_graph(intensive_data, angle_data, intensive_data_2, angle_data_2)
    # draw_lines(intensive_data, angle_data, wave_length, end_angle, intensive_data_2, angle_data_2)

root = tk.Tk()
root.title("Graph Plotter")

fields = [
    ("Количество разбиений", "2"),
    ("Ширина разбиений", "0.001"),
    ("Период", "0.005"),
    ("Длина волны", "400e-9"),
    ("Конечный угол", "0.001"),
    ("Количество шагов", "10000")
]

entries = {}
for field, default in fields:
    frame = tk.Frame(root)
    label = tk.Label(frame, text=field)
    entry = tk.Entry(frame)
    entry.insert(0, default)
    label.pack(side="left")
    entry.pack(side="right")
    frame.pack(fill="x", padx=10, pady=5)
    entries[field] = entry

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=20)

root.mainloop()

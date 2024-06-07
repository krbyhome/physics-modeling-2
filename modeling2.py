import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def in_range(x, a, b):
    return a <= x and x <= b 

def wavelength_to_rgb(wavelength):
    gamma = 0.80
    intensity_max = 255
    colors = {'red': 0.0, 'green': 0.0, 'blue': 0.0}

    # Диапазоны длины волны и соответствующие значения цветов
    ranges = [
        ((380, 440), {'red': lambda x: (440 - x) / (440 - 380), 'blue': 1.0}),
        ((440, 490), {'green': lambda x: (x - 440) / (490 - 440), 'blue': 1.0}),
        ((490, 510), {'green': 1.0, 'blue': lambda x: (510 - x) / (510 - 490)}),
        ((510, 580), {'red': lambda x: (x - 510) / (580 - 510), 'green': 1.0}),
        ((580, 645), {'red': 1.0, 'green': lambda x: (645 - x) / (645 - 580)}),
        ((645, 781), {'red': 1.0}),
    ]

    # Определение цветовых компонент
    for (start, end), color_values in ranges:
        if start <= wavelength < end:
            for color, value in color_values.items():
                if callable(value):
                    colors[color] = value(wavelength)
                else:
                    colors[color] = value

    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength < 701:
        factor = 1.0
    elif 701 <= wavelength < 781:
        factor = 0.3 + 0.7 * (780 - wavelength) / (780 - 700)
    else:
        factor = 0.0

    for color in colors:
        if colors[color] != 0:
            colors[color] = round(intensity_max * (colors[color] * factor) ** gamma)

    return [colors['red'], colors['green'], colors['blue']]

def run_simulation():
    d = float(entry_d.get())
    N = float(entry_N.get())

    lambda1 = float(entry_lambda1.get())
    lambda2 = float(entry_lambda2.get())
    lambda3 = float(entry_lambda3.get())
    lambdas = [lambda1, lambda2, lambda3]

    def intensity(theta, wavelength):
        beta = (np.pi * d * np.sin(theta)) / wavelength
        return (np.sin(N * beta) / np.sin(beta)) ** 2 * (np.sinc(beta / np.pi)) ** 2

    if not (in_range(lambda1, d / 10, d * 10) and in_range(lambda2, d / 10, d * 10)):
        print('Дифракционная картина не может наблюдаться, будет сплошной спектр (d << alpha)')
        exit()

    theta = np.linspace(-np.pi / 1000, np.pi / 1000, 10000)

    intensities = list(map(lambda k: intensity(theta, k), lambdas))

    plt.figure(figsize=(10, 10))
    plt.subplot(2, 1, 1)
    for i in intensities:
        plt.plot(np.degrees(theta), i)
    plt.xlabel('Угол дифракции (градусы)')
    plt.ylabel('Интенсивность')
    plt.title(f'Дифракционная картина для {len(intensities)} близких спектральных линий')
    plt.grid(True)

    width = len(theta)
    height = 100
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(width):
        wavelength = lambda1 if intensities[0][i] > intensities[1][i] else lambda2
        color = wavelength_to_rgb(wavelength * 1e9)
        image[:, i] = color
    
    plt.subplot(2, 1, 2)
    plt.imshow(image, aspect='auto', extent=(-np.pi / 1000, np.pi / 1000, 0, 1))
    plt.xlabel('Угол дифракции (градусы)')
    plt.yticks([])
    plt.title('Цветной дифракционный спектр')
    plt.show()


root = tk.Tk()
root.title("Параметры системы")

fields = [
    ("период решетки в метрах", "1e-6"),
    ("Число штрихов", "1500"),
    ("Длина волны 1 в метрах", "460e-9"),
    ("Длина волны 2 в метрах", "510e-9"),
    ("Длина волны 3 в метрах", "550e-9"),
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

entry_d = entries["период решетки в метрах"]
entry_N = entries["Число штрихов"]
entry_lambda1 = entries["Длина волны 1 в метрах"]
entry_lambda2 = entries["Длина волны 2 в метрах"]
entry_lambda3 = entries["Длина волны 3 в метрах"]

button = ttk.Button(root, text="Запустить симуляцию", command=run_simulation)
button.pack(pady=20)

root.mainloop()

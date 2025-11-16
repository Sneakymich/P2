import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from matplotlib.patches import Patch

# === 1. Cargar la señal de audio ===
sr, signal = wavfile.read('audio.wav')  # sr = sample rate
signal = signal / np.max(np.abs(signal))  # Normalizar
duration = len(signal) / sr
time_axis = np.linspace(0, duration, len(signal))

# === 2. Leer etiquetas desde archivos ===
def read_labels(filepath, sep):
    labels = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(sep)
            if len(parts) == 3:
                start, end, label = parts
                labels.append((float(start), float(end), label))
    return labels

manual_labels = read_labels('audio.lab', sep=' ')
auto_labels = read_labels('audio.vad', sep='\t')

# === 3. Agrupar segmentos consecutivos con la misma etiqueta ===
def merge_consecutive_labels(labels):
    if not labels:
        return []

    merged = [labels[0]]
    for start, end, label in labels[1:]:
        last_start, last_end, last_label = merged[-1]
        # Si es el mismo tipo y es continuo en el tiempo, los unimos
        if label == last_label and abs(start - last_end) < 1e-6:
            merged[-1] = (last_start, end, label)
        else:
            merged.append((start, end, label))
    return merged

merged_auto_labels = merge_consecutive_labels(auto_labels)

# === 4. Graficar ===
plt.figure(figsize=(14, 6))
plt.plot(time_axis, signal, color='gray', alpha=0.6, label='Señal de voz audio.wav') # Parametro alpha: transparencia

# Etiquetas manuales: línea horizontal en y = -1.10
for start, end, label in manual_labels:
    color = 'blue' if label == 'V' else 'red'
    plt.fill_betweenx([-1.10, -1.00], start, end, color=color, alpha=0.8)

# Etiquetas automáticas: línea horizontal en y = -1.25
for start, end, label in merged_auto_labels:
    color = 'blue' if label == 'V' else 'red'
    plt.fill_betweenx([-1.25, -1.15], start, end, color=color, alpha=0.8)

# Etiquetas de texto
plt.text(duration, -1.020, 'Manual', va='center', fontsize=10, color='black')
plt.text(duration, -1.18, 'Auto', va='center', fontsize=10, color='black')

# Leyendas:
legend_elements = [
    Patch(facecolor='blue', edgecolor='black', label='Voz'),
    Patch(facecolor='red', edgecolor='black', label='Silencio')
]

plt.legend(handles=legend_elements, title='Etiquetas', loc='upper left')

# Configuración final del gráfico
plt.ylim(-1.4, 1.2)
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.title('Señal de voz vs etiquetado manual (.lab) vs etiquetado automático (.vad) con alpha1 = 10,7 ')
plt.tight_layout()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.show()
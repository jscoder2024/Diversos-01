import tkinter as tk
from tkinter import filedialog, ttk
import sounddevice as sd
import soundfile as sf
import numpy as np

class Pad:
    def __init__(self, master, nome, cor, row, column):
        self.master = master
        self.nome = nome
        self.cor = cor
        
        self.frame = tk.Frame(master, bd=1, relief=tk.RAISED)
        self.frame.grid(row=row, column=column, padx=3, pady=3)

        self.button = tk.Button(self.frame, text=nome, bg=cor, fg='white', font=('Arial', 8),
                                command=self.play_sound, width=8)
        self.button.pack(pady=2)

        self.volume_slider = tk.Scale(self.frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL,
                                       label="Vol", length=80)
        self.volume_slider.set(1)  # Volume padrão 100%
        self.volume_slider.pack(pady=2)

        self.is_playing = False
        self.data = None
        self.samplerate = None

        # Botão para carregar o arquivo de áudio
        self.load_button = tk.Button(self.frame, text="Carregar", command=self.load_sound, width=8)
        self.load_button.pack(pady=2)

        self.pause_button = tk.Button(self.frame, text="Pausar", command=self.pause_sound, width=8)
        self.pause_button.pack(pady=2)

        self.stop_button = tk.Button(self.frame, text="Parar", command=self.stop_sound, width=8)
        self.stop_button.pack(pady=2)

    def load_sound(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if arquivo:
            self.data, self.samplerate = sf.read(arquivo)

    def play_sound(self):
        if self.data is not None and not self.is_playing:
            sd.play(self.data * self.volume_slider.get(), self.samplerate)
            self.is_playing = True
            self.button.config(relief=tk.SUNKEN)  # Indicar que está tocando

    def pause_sound(self):
        if self.is_playing:
            sd.stop()
            self.is_playing = False
            self.button.config(relief=tk.RAISED)  # Resetar o botão

    def stop_sound(self):
        sd.stop()
        self.is_playing = False
        self.button.config(relief=tk.RAISED)  # Resetar o botão


class Equalizer:
    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(master)
        self.frame.pack(pady=10)

        self.label_low = tk.Label(self.frame, text="Graves")
        self.label_low.pack()
        self.low_slider = tk.Scale(self.frame, from_=-10, to=10, orient=tk.HORIZONTAL)
        self.low_slider.set(0)
        self.low_slider.pack()

        self.label_mid = tk.Label(self.frame, text="Médios")
        self.label_mid.pack()
        self.mid_slider = tk.Scale(self.frame, from_=-10, to=10, orient=tk.HORIZONTAL)
        self.mid_slider.set(0)
        self.mid_slider.pack()

        self.label_high = tk.Label(self.frame, text="Agudos")
        self.label_high.pack()
        self.high_slider = tk.Scale(self.frame, from_=-10, to=10, orient=tk.HORIZONTAL)
        self.high_slider.set(0)
        self.high_slider.pack()

        # Adicione outros controles de equalização conforme necessário

    def apply_eq(self, data):
        # Aqui você pode aplicar os efeitos de equalização
        low_gain = 10 ** (self.low_slider.get() / 20)  # Conversão de dB para ganho
        mid_gain = 10 ** (self.mid_slider.get() / 20)
        high_gain = 10 ** (self.high_slider.get() / 20)

        # Exemplo simples de equalização (não é um EQ real, apenas ilustrativo)
        # Esta parte deve ser substituída por lógica de equalização real.
        # Você poderia usar filtros, FFT, etc. para uma equalização mais sofisticada.
        eq_data = data * [low_gain, mid_gain, high_gain]
        return eq_data


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Padusical")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10)

        self.pad_frame = tk.Frame(self.notebook)
        self.equalizer_frame = Equalizer(self.notebook)

        self.notebook.add(self.pad_frame, text="Pads")
        self.notebook.add(self.equalizer_frame.frame, text="Equalizador")

        # Lista de nomes e cores para os pads (18 pads)
        pads = [
            ("Pad 1", "red"),
            ("Pad 2", "orange"),
            ("Pad 3", "yellow"),
            ("Pad 4", "green"),
            ("Pad 5", "blue"),
            ("Pad 6", "indigo"),
            ("Pad 7", "violet"),
            ("Pad 8", "pink"),
            ("Pad 9", "cyan"),
            ("Pad 10", "magenta"),
            ("Pad 11", "brown"),
            ("Pad 12", "gray"),
            ("Pad 13", "lightblue"),
            ("Pad 14", "lightgreen"),
            ("Pad 15", "lightyellow"),
            ("Pad 16", "lightcoral"),
            ("Pad 17", "lightsalmon"),
            ("Pad 18", "lightpink"),
        ]

        self.pads = []
        for index, (nome, cor) in enumerate(pads):
            row = index // 6  # 6 pads por linha
            column = index % 6
            pad = Pad(self.pad_frame, nome, cor, row, column)
            self.pads.append(pad)

# Criação da janela principal
root = tk.Tk()
app = App(root)

# Inicia o loop principal
root.mainloop()


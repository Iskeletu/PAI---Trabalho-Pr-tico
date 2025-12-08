"""Block class defition file for PSE_GUI."""

# Internal Modules:
import tkinter as tk

# External Modules:
import numpy as np
import matplotlib.pyplot as mpl


class Block:
    """
    Main parent class: every inherited child class will input and output an image.

    Methods:
        - `apply`: Raises `NotImplementedError` if the inherited class does not implement its own apply method.
    
    """

    def apply(self, image:np.ndarray) -> np.ndarray:
        """Applies the transformation to the image."""

        raise NotImplementedError


class BrightnessBlock(Block):
    def __init__(self, delta_var: tk.StringVar):
        self.delta_var = delta_var

    def apply(self, image: np.ndarray) -> np.ndarray:
        try:
            delta = int(self.delta_var.get())
        except ValueError:
            delta = 0

        # trabalha em maior precisão pra evitar overflow
        tmp = image.astype(np.int16) + delta
        tmp = np.clip(tmp, 0, 255)
        return tmp.astype(np.uint8)


class ThresholdBlock(Block):
    def __init__(self, threshold_var: tk.StringVar):
        self.threshold_var = threshold_var

    def apply(self, image: np.ndarray) -> np.ndarray:
        try:
            t = int(self.threshold_var.get())
        except ValueError:
            t = 128

        t = max(0, min(255, t))
        result = np.zeros_like(image, dtype=np.uint8)
        result[image >= t] = 255
        return result


class HistogramBlock(Block):
    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Mostra o histograma da imagem, mas não altera a imagem.
        """
        hist, _ = np.histogram(image.flatten(), bins=256, range=(0, 255))
        mpl.figure()
        mpl.bar(range(256), hist)
        mpl.title("Histograma")
        mpl.xlabel("Intensidade")
        mpl.ylabel("Frequência")
        mpl.show()
        return image


class ConvolutionBlock(Block):
    def __init__(self, kernel_entries: list[tk.Entry]):
        self.kernel_entries = kernel_entries  # entradas 3x3

    def get_kernel(self) -> np.ndarray:
        vals = []
        for e in self.kernel_entries:
            try:
                vals.append(float(e.get()))
            except ValueError:
                vals.append(0.0)
        kernel = np.array(vals).reshape((3, 3))
        return kernel

    def apply(self, image: np.ndarray) -> np.ndarray:
        kernel = self.get_kernel()
        k = kernel.shape[0]  # 3
        pad = k // 2         # 1

        # padding com zeros
        padded = np.pad(
            image.astype(np.float32),
            pad_width=pad,
            mode="constant",
            constant_values=0,
        )

        h, w = image.shape
        out = np.zeros_like(image, dtype=np.float32)

        # convolução "na mão"
        for i in range(h):
            for j in range(w):
                region = padded[i:i + k, j:j + k]
                out[i, j] = np.sum(region * kernel)

        out = np.clip(out, 0, 255)
        return out.astype(np.uint8)
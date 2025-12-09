"""Block class defition file for PSE_GUI."""

# Native Modules:
import tkinter as tk

# Internal Modules:
import FileHandling.image_reading as IR

# External Modules:
import numpy as np
import matplotlib.pyplot as mpl
from pathlib import Path


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


class DifferenceBlock(Block):
    """
    Bloco que calcula a diferença entre a imagem atual do pipeline
    e uma outra imagem RAW escolhida pelo usuário.

    A outra imagem é definida por:
    - caminho do arquivo RAW
    - largura e altura informadas no próprio bloco
    """

    def __init__(
        self,
        path_var: tk.StringVar,
        width_var: tk.StringVar,
        height_var: tk.StringVar,
    ) -> None:
        self._path_var = path_var
        self._width_var = width_var
        self._height_var = height_var

    def apply(self, image: np.ndarray) -> np.ndarray:
        # pega dados da interface
        path_str = self._path_var.get()
        if not path_str:
            raise ValueError("Nenhum arquivo RAW selecionado no bloco de diferença.")

        try:
            w = int(self._width_var.get())
            h = int(self._height_var.get())
        except ValueError:
            raise ValueError("Largura e/ou altura inválidas no bloco de diferença.")

        if w <= 0 or h <= 0:
            raise ValueError("Largura e altura devem ser positivas no bloco de diferença.")

        path = Path(path_str)

        # lê a segunda imagem RAW
        reader = IR.RawImageReader(path, w, h)
        other = reader.image

        # checa se tem o mesmo tamanho da imagem atual do pipeline
        if other.shape != image.shape:
            raise ValueError(
                f"As imagens devem ter o mesmo tamanho para a diferença.\n"
                f"Imagem do pipeline: {image.shape}, outra imagem: {other.shape}"
            )

        # diferença absoluta |img1 - img2|
        a = image.astype(np.int16)
        b = other.astype(np.int16)
        diff = np.abs(a - b)
        diff = np.clip(diff, 0, 255).astype(np.uint8)

        return diff
"""Block class defition file for PSE_GUI."""

# Native Modules:
import tkinter as tk

# Internal Modules:
import PSE.image_display as ID
import FileHandling.image_reading as IR

# External Modules:
import numpy as np
from pathlib import Path
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


class DisplayBlock(Block):
    """
    Bloco de exibição de imagem.

    Mostra a imagem atual usando o módulo PSE.image_display e
    devolve a mesma imagem (não altera o pipeline).
    """

    def __init__(self, title_var: tk.StringVar | None = None) -> None:
        self._title_var = title_var

    def apply(self, image: np.ndarray) -> np.ndarray:
        title = self._title_var.get() if self._title_var is not None else "Imagem"
        ID.display(image, title)
        return image


class SaveRawBlock(Block):
    """
    Bloco de gravação RAW.

    Salva a imagem atual em um arquivo .raw (8 bits, grayscale),
    sem cabeçalho. Não altera a imagem do pipeline.
    """

    def __init__(self, path_var: tk.StringVar) -> None:
        self._path_var = path_var

    def apply(self, image: np.ndarray) -> np.ndarray:
        path_str = self._path_var.get()
        if not path_str:
            raise ValueError("Nenhum arquivo de saída definido no bloco de gravação RAW.")

        file_path = Path(path_str)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        arr = np.clip(image, 0, 255).astype(np.uint8)
        file_path.write_bytes(arr.tobytes())

        return image


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
    """
    Bloco de convolução local.

    - O tamanho do kernel é inferido de `entries_matrix` (n x n).
    - Os pesos são lidos das entradas de texto.
    """

    def __init__(self, size_var, entries_matrix) -> None:
        # size_var: tk.StringVar (usado só pra GUI)
        # entries_matrix: list[list[tk.Entry]]
        self._size_var = size_var
        self._entries_matrix = entries_matrix

    def set_entries_matrix(self, entries_matrix) -> None:
        """Atualiza a referência da matriz de entradas (quando a GUI recria o grid)."""
        self._entries_matrix = entries_matrix

    def _get_kernel(self) -> np.ndarray:
        if not self._entries_matrix:
            raise RuntimeError("Kernel não definido: matriz de entradas vazia.")

        n = len(self._entries_matrix)
        values: list[float] = []

        for row in self._entries_matrix:
            # garante que é uma linha com n colunas
            if len(row) != n:
                raise RuntimeError("Matriz de entradas não é quadrada.")
            for e in row:
                try:
                    values.append(float(e.get()))
                except Exception:
                    values.append(0.0)

        kernel = np.asarray(values, dtype=float).reshape((n, n))
        return kernel

    def apply(self, image: np.ndarray) -> np.ndarray:
        kernel = self._get_kernel()
        k = kernel.shape[0]
        pad = k // 2

        # padding com zeros
        padded = np.pad(
            image.astype(np.float32),
            pad_width=pad,
            mode="constant",
            constant_values=0,
        )

        h, w = image.shape
        out = np.zeros((h, w), dtype=np.float32)

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
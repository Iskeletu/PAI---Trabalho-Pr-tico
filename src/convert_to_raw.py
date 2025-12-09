"""Functions to convert normal images to RAW (8 bits, grayscale)"""

# Native Modules:
import sys
from pathlib import Path

# Internal Modules:
from constants import TARGET_WIDTH, TARGET_HEIGHT

# External Modules:
import numpy as np
from PIL import Image


def _image_to_raw_grayscale(input_file_path:Path, output_folder_path:Path) -> None:
    input_file_path = Path(input_file_path)
    output_folder_path = Path(output_folder_path)

    if not input_file_path.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_file_path}")

    img = Image.open(input_file_path)
    img = img.convert("RGB")

    img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.BILINEAR)

    arr = np.asarray(img, dtype=np.float32)

    r = arr[..., 0]
    g = arr[..., 1]
    b = arr[..., 2]

    # Converte para escala de cinza usando luminância aproximada (BT.601)
    # gray = 0.299*R + 0.587*G + 0.114*B
    gray = 0.299 * r + 0.587 * g + 0.114 * b

    # Garante faixa 0–255 e tipo uint8
    gray = np.clip(gray, 0, 255).astype(np.uint8)

    # Pega dimensões
    height, width = gray.shape

    # Salva só os bytes dos pixels (RAW puro, sem cabeçalho)
    output_file_path:Path = (output_folder_path / f"raw_image_{width}w_{height}h.raw").absolute()
    output_file_path.write_bytes(gray.tobytes())

    print(f"Imagem de entrada: {input_file_path}")
    print(f"Dimensões (LxA): {width} x {height}")
    print(f"Arquivo RAW salvo em: {output_file_path}")


def main() -> None:
    """"""

    if len(sys.argv) != 3:
        print("Uso:")
        print("  python image_to_raw.py <path/input_file.(png|jpg|etc.)> <output_path/>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_folder_path = sys.argv[2]

    try:
        _image_to_raw_grayscale(input_file_path, output_folder_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# This is a script file and should NOT be imported:
if __name__ == '__main__':
    main()
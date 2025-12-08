"""
File reading implementation.
"""

# Native Modules:
from pathlib import Path
from typing import Tuple

# Internal Modules:
from constants import INPUT_FILE_PATH

# External Modules:
import numpy as np
import matplotlib.pyplot as mpl

# Constants:


class RawImageReader:
    """
    RAW image file reader (8 bits, grayscale).

    Methods:
        - `dimensions` (@property): Property type method that returns the image
        dimensions as a list, position 0 being width and position 1 being height.

    Private Methods:
        - `_read_image`: Reads RAW image files and processes it as a NumPy array
        with format (_height, _width) and dtype `uint8`.
    """

    def __init__(self, file_name:str, width:int, height:int) -> None:
        """
        Initializes an instance of GuiCommand class.

        Parameters:
            - file_name: String containing the image file name (with file
            extension) to be searched in the input directory.
            - width: Image width in pixels.
            - height: Image height in pixels.
        """

        if int(width) <= 0 or int(height) <= 0:
            raise ValueError("Image width and height must be positive!")

        self._width:int             = int(width)
        self._height:int            = int(height)
        self._expected_size:int     = (int(width) * int(height))

        self._raw_image:np.ndarray  = self._read_image(file_name)

    @property
    def dimensions(self) -> list[int, int]:
        """
        Returns image reader object file dimensions (in pixels) as a list,
        position 0 being width and position 1 being height.

        Usage:
            >>> dimensions:list[int, int] = reader.dimensions
        """

        return [self._width, self._height]

    def _read_image(self, file_name:str) -> np.ndarray:
        """
        Reads RAW image files and processes it as a NumPy array with format
        (_height, _width) and dtype `uint8`.

        Parameters:
            - file_name: String containing the image file name (with file
            extension) to be searched in the input directory.

        Return:
            The image data as a shaped numpy.ndarray (height, width) and dtype `uint8`.
        """
        
        FILE_PATH:Path = (INPUT_FILE_PATH / file_name).resolve()

        if not FILE_PATH.exists():
            raise FileNotFoundError(f"File not found: {FILE_PATH}")

        raw_data = FILE_PATH.read_bytes()

        if len(raw_data) != self._expected_size:
            raise ValueError(
                f"file size ({len(raw_data)} bytes) does not match the "
                f"expected image ({self._expected_size} bytes = "
                f"{self._width}x{self._height})."
            )

        raw_image = np.frombuffer(raw_data, dtype=np.uint8)
        raw_image = raw_image.reshape((self._height, self._width))

        return raw_image

    def display_image(self) -> None:
        """
        Displays object image.
        """

        mpl.imshow(self._raw_image, cmap="gray", vmin=0, vmax=255)
        mpl.axis("off")
        mpl.show()



# This is NOT a script file.
if __name__ == '__main__':
    raise RuntimeError("This module is not a standalone script.")
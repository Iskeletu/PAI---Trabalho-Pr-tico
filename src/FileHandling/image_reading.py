"""
Image file reading implementation (normal and raw).
"""

# Native Modules:
from pathlib import Path

# Internal Modules:
import PSE.image_display as ID

# External Modules:
import numpy as np


class RawImageReader:
    """
    RAW image file reader (8 bits, grayscale).

    Private_Attributes:
        - 

    Methods:
        - `dimensions` (@property): Property type method that returns the image
        dimensions as a list, position 0 being width and position 1 being height.
        - `image` (@property): Property type method that returns the image data
        as a numpy.ndarray object.

    Private Methods:
        - `_read_image`: Reads RAW image files and processes it as a NumPy array
        with format (_height, _width) and dtype `uint8`.
    """

    def __init__(self, file_path:str|Path, width:int, height:int) -> None:
        """
        Initializes an instance of RawImageReader class.

        Parameters:
            - file_path: A string or a PathLib.Path object to the image file to be read.
            - width: Image width in pixels.
            - height: Image height in pixels.
        """

        if int(width) <= 0 or int(height) <= 0:
            raise ValueError("Image width and height must be positive!")

        self._width:int             = int(width)
        self._height:int            = int(height)
        self._expected_size:int     = (int(width) * int(height))

        self._raw_image:np.ndarray  = self._read_image(Path(file_path))

    @property
    def dimensions(self) -> list[int, int]:
        """
        Returns image reader object file dimensions (in pixels) as a list,
        position 0 being width and position 1 being height.

        Usage:
            >>> dimensions:list[int, int] = reader.dimensions
        """

        return [self._width, self._height]

    @property
    def image(self) -> np.ndarray:
        """
        Returns the raw image data from the image reader object as a numpy.ndarray
        object.

        Usage:
            >>> image:numpy.ndarray = reader.image
        """

        return self._raw_image

    def _read_image(self, file_path:Path) -> np.ndarray:
        """
        Reads RAW image files and processes it as a NumPy array with format
        (_height, _width) and dtype `uint8`.

        Parameters:
            - file_path: A PathLib.Path object to the image file to be read.

        Return:
            The image data as a shaped numpy.ndarray (height, width) and dtype `uint8`.
        """

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        raw_data = file_path.read_bytes()

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

        ID.display(self._raw_image)



# This is NOT a script file.
if __name__ == '__main__':
    raise RuntimeError("This module is not a standalone script.")
    
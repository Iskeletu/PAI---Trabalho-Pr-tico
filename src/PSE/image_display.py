"""
"""

# Internal Modules:
from constants import PROJECT_NAME

# External Modules:
import numpy as np
import matplotlib.pyplot as mpl


def display(image:np.ndarray, title:str|None=None) -> None:
    """
    This functions displays a numpy.ndarray to the screen using MatPlotLib.

    Parameters:
        - image: The numpy.ndarray object to be displayed as an image.
        - title: Optional -> A string to be displayed as the image title.
    """

    fig = mpl.figure()
    fig.canvas.manager.set_window_title(PROJECT_NAME)

    mpl.imshow(image, cmap="gray", vmin=0, vmax=255)
    if title: mpl.title(title)
    mpl.axis("off")

    mpl.show()


# This is NOT a script file.
if __name__ == '__main__':
    raise RuntimeError("This module is not a standalone script.")

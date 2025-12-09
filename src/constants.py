"""
Constant values definition module.
* None of these values should change during runtime.
"""

# Native Modules:
from pathlib import Path
from typing import Final


# Constants:
PROJECT_NAME:Final[str] = "Processamento e Análise de Imagens - Trabalho prático"

_PROJECT_FILE_PATH:Path = (Path(__file__).parent.parent).resolve()  # Project file directory absolute path (as a pathlib Path object).
INPUT_FOLDER_PATH:Path    = (_PROJECT_FILE_PATH / "input/").resolve()  # Image input file directory absolute path (as a pathlib Path object).
OUTPUT_FOLDER_PATH:Path   = (_PROJECT_FILE_PATH / "output/").resolve() # Image output file directory absolute path (as a pathlib Path object).

TARGET_WIDTH:Final[int]     = 640 # Target image width for image conversion to raw file. 
TARGET_HEIGHT:Final[int]    = 360 # Target image height for image conversion to raw file.


# This is NOT a script file.
if __name__ == '__main__':
    raise RuntimeError("This module is not a standalone script.")
"""GUI handling file for PSE."""

# Native Modules:
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

# Internal Modules:
import PSE.blocks as blocks
import PSE.image_display as ID
import FileHandling.image_reading as IR


class PSE_GUI:
    """
    PSE Tkinter GUi class.

    Private Attributes:
        - `_root`: Top level widget.
        - `_path_var`: String with the file path to the selected file.
        - `_width_var`: Integer number of columns of pixel the read raw image has.
        - `_height_var`: Integer number of rows of pixel the read raw image has.
        - `_blocks`: List of ordered user selected blocks within the PSE_GUI app.
        - `_blocks_frame`: Tkinter frame widget where the list of blocks selected
        by the user within the PSE_GUI interface is displayed.

    Private Methods:
        - `_create_sections`: Creates the base widget structure of the app.
        - `_browse_file`: Opens explorer file handler and get the selected file path.
        - `_add_brightness_block`: Adds the brightness block to the end of the pipeline.
        - `_add_threshold_block`: Adds the threshold block to the end of the pipeline.
        - `_add_histogram_block`: Adds the histogram block to the end of the pipeline.
        - `_add_convolution_block`: Adds the convolution block to the end of the pipeline.
        - `_process_pipeline`: Executes the constructed pipeline.
        - `_reset_app`: Resets all the widgets to the original configuration.
    """

    def __init__(self, root:tk.Tk) -> None:
        """Creates a new instance of PSE_GUI class"""

        self._root = root
        self._root.title("Problem Solving Environment")

        self._create_sections()

    #------------------------- Interface Sections -------------------------
    def _create_sections(self) -> None:
        """
        Initial Tkinter app widget sctructure.
        """

        #------------------ RAW image file selection section ------------------
        top = tk.Frame(self._root)
        top.pack(fill="x", padx=5, pady=5)

        tk.Label(top, text="Arquivo RAW:").grid(row=0, column=0, sticky="w")
        self._path_var = tk.StringVar()
        tk.Entry(top, textvariable=self._path_var, width=40).grid(
            row=0, column=1, sticky="we"
        )
        tk.Button(top, text="Procurar...", command=self._browse_file).grid(
            row=0, column=2, padx=5
        )

        tk.Label(top, text="Largura:").grid(row=1, column=0, sticky="w")
        self._width_var = tk.StringVar(value="506")
        tk.Entry(top, textvariable=self._width_var, width=8).grid(
            row=1, column=1, sticky="w"
        )

        tk.Label(top, text="Altura:").grid(row=1, column=2, sticky="w")
        self._height_var = tk.StringVar(value="360")
        tk.Entry(top, textvariable=self._height_var, width=8).grid(
            row=1, column=3, sticky="w"
        )
        #----------------------------------------------------------------------

        #------------------------ Block Insertion Zone ------------------------
        self._blocks_frame = tk.LabelFrame(
            self._root, text="Blocos de processamento (em sequência)"
        )
        self._blocks_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self._blocks:list[blocks.Block] = []
        #----------------------------------------------------------------------

        #--------------------------- Control Buttons --------------------------
        buttons_frame = tk.Frame(self._root)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(
            buttons_frame,
            text="Adicionar brilho",
            command=self._add_brightness_block,
        ).pack(side="left", padx=2)

        tk.Button(
            buttons_frame,
            text="Adicionar limiarização",
            command=self._add_threshold_block,
        ).pack(side="left", padx=2)

        tk.Button(
            buttons_frame,
            text="Adicionar convolução 3x3",
            command=self._add_convolution_block,
        ).pack(side="left", padx=2)

        tk.Button(
            buttons_frame,
            text="Adicionar histograma",
            command=self._add_histogram_block,
        ).pack(side="left", padx=2)

        control_frame = tk.Frame(self._root)
        control_frame.pack(padx=5, pady=5)

        tk.Button(
            control_frame,
            text="Processar fluxo",
            command=self._process_pipeline
        ).pack(side="left", padx=5)

        tk.Button(
            control_frame,
            text="Redefinir",
            command=self._reset_app
        ).pack(side="left", padx=5)
        #----------------------------------------------------------------------
    #----------------------------------------------------------------------

    #------------------------- Interface Callbacks ------------------------
    def _browse_file(self) -> None:
        """
        Opens the explorer file navigation handler.
        """
        
        path = filedialog.askopenfilename(
            filetypes=[("RAW files", "*.raw"), ("Todos os arquivos", "*.*")]
        )
        if path:
            self._path_var.set(path)

    def _add_brightness_block(self) -> None:
        """
        Adds a brightness block to the end of the pipeline in the blocks section of the interface.
        """

        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        tk.Label(frame, text="Brilho Δ:").pack(side="left")
        delta_var = tk.StringVar(value="0")
        tk.Entry(frame, textvariable=delta_var, width=8).pack(side="left")

        block = blocks.BrightnessBlock(delta_var)
        self._blocks.append(block)

    def _add_threshold_block(self) -> None:
        """
        Adds a treshold block to the end of the pipeline in the blocks section of the interface.
        """
        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        tk.Label(frame, text="Limiar T:").pack(side="left")
        t_var = tk.StringVar(value="128")
        tk.Entry(frame, textvariable=t_var, width=8).pack(side="left")

        block = blocks.ThresholdBlock(t_var)
        self._blocks.append(block)

    def _add_histogram_block(self):
        """
        Adds a histogram block to the end of the pipeline in the blocks section of the interface.
        """
        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        tk.Label(frame, text="Histograma").pack(side="left")

        block = blocks.HistogramBlock()
        self._blocks.append(block)

    def _add_convolution_block(self) -> None:
        """
        Adds a convolution block to the end of the pipeline in the blocks section of the interface.
        """
        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        tk.Label(frame, text="Convolução 3x3 (kernel):").pack(
            side="top", anchor="w"
        )

        grid_frame = tk.Frame(frame)
        grid_frame.pack()

        entries = []
        for i in range(3):
            for j in range(3):
                e = tk.Entry(grid_frame, width=4)
                e.grid(row=i, column=j, padx=1, pady=1)
                e.insert(0, "0")
                entries.append(e)

        block = blocks.ConvolutionBlock(entries)
        self._blocks.append(block)

    def _process_pipeline(self):
        """
        Executes the pipeline created by the user in the interface, the execution order is top to bottom.
        """
        
        file_path = self._path_var.get()
        if not file_path:
            messagebox.showerror("Erro", "Selecione um arquivo .RAW!")
            return
        file_path = Path(file_path)

        try:
            width = int(self._width_var.get())
            height = int(self._height_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Largura e/ou altura inválidas!")
            return

        try:
            reader = IR.RawImageReader(file_path, width, height)
        except Exception as e:
            messagebox.showerror("Erro ao ler RAW", str(e))
            return


        current = reader.image
        ID.display(current, "Imagem Inicial:")
        for block in self._blocks:
            current = block.apply(current)
        ID.display(current, "Imagem Final:")

    def _reset_app(self) -> None:
        """
        Resets the entire GUI.
        """

        for child in self._root.winfo_children():
            child.destroy()

        self._create_sections()
    #----------------------------------------------------------------------


def start() -> None:
    """
    Tkinter setup function, starts the GUI.
    """

    root = tk.Tk()
    PSE_GUI(root)
    root.mainloop() 


# This is NOT a script file.
if __name__ == '__main__':
    raise RuntimeError("This module is not a standalone script.")

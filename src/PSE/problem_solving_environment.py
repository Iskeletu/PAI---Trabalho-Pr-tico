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
        - `_add_difference_block`: Adds the difference block to the end of the pipeline.
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
        self._width_var = tk.StringVar(value="640")
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
            text="Exibir Imagem",
            command=self._add_display_block,
        ).pack(side="left", padx=2)

        tk.Button(
            buttons_frame,
            text="Salvar .RAW",
            command=self._add_saveraw_block,
        ).pack(side="left", padx=2)

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

        tk.Button(
            buttons_frame,
            text="Adicionar diferença",
            command=self._add_difference_block,
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

    def _add_display_block(self) -> None:
        """
        Adds a display block to the end of the pipeline in the blocks section of the interface.
        Shows the current image when executed.
        """

        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        tk.Label(frame, text="Exibir imagem").pack(side="left")

        # Título opcional da janela de exibição
        title_var = tk.StringVar(
            value=f"Imagem após bloco {len(self._blocks)}"
        )
        tk.Entry(frame, textvariable=title_var, width=30).pack(
            side="left", padx=4
        )

        block = blocks.DisplayBlock(title_var)
        self._blocks.append(block)

    def _add_saveraw_block(self) -> None:
        """
        Adds a save raw block to the end of the pipeline in the blocks section of the interface.
        Saves the current image to a .raw file.
        """

        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        tk.Label(frame, text="Gravar imagem RAW").pack(side="left")

        file_frame = tk.Frame(frame)
        file_frame.pack(side="left", padx=4)

        path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=path_var, width=30).pack(
            side="left", padx=(0, 2)
        )

        def browse_save():
            path = filedialog.asksaveasfilename(
                defaultextension=".raw",
                filetypes=[("RAW files", "*.raw"), ("Todos os arquivos", "*.*")],
            )
            if path:
                path_var.set(path)

        tk.Button(file_frame, text="...", command=browse_save, width=3).pack(
            side="left"
        )

        block = blocks.SaveRawBlock(path_var)
        self._blocks.append(block)

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
        Adds a convolution block to the end of the pipeline in the blocks section
        of the interface.

        - Allows the user to choose the size of the mask (3x3, 5x5, 7x7, 9x9).
        - Include preset masks: Avarege, Laplaciano (4 / 8 neighbours).
        """

        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        header_frame = tk.Frame(frame)
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="Convolução local").pack(side="left")

        tk.Label(header_frame, text="  Tamanho:").pack(side="left", padx=(10, 2))
        size_var = tk.StringVar(value="3")
        size_spin = tk.Spinbox(
            header_frame,
            from_=1,
            to=9,
            increment=2,          # 1, 3, 5, 7, 9...
            width=4,
            textvariable=size_var,
        )
        size_spin.pack(side="left")

        tk.Label(header_frame, text="  Máscara:").pack(side="left", padx=(10, 2))
        preset_var = tk.StringVar(value="Personalizada")
        preset_menu = tk.OptionMenu(
            header_frame,
            preset_var,
            "Personalizada",
            "Média",
            "Laplaciano (4-vizinhos)",
            "Laplaciano (8-vizinhos)",
        )
        preset_menu.pack(side="left")

        grid_frame = tk.Frame(frame)
        grid_frame.pack(pady=2)

        entries_matrix: list[list[tk.Entry]] = []

        conv_block = blocks.ConvolutionBlock(size_var, entries_matrix)
        self._blocks.append(conv_block)

        def build_grid(*_args):
            """
            (Re)construct the input grid given choosen size.
            """
            nonlocal entries_matrix

            # Clears previous grid:
            for child in grid_frame.winfo_children():
                child.destroy()
            entries_matrix = []

            try:
                n = int(size_var.get())
            except ValueError:
                n = 3

            if n < 1:
                n = 1

            for i in range(n):
                row: list[tk.Entry] = []
                for j in range(n):
                    e = tk.Entry(grid_frame, width=4)
                    e.grid(row=i, column=j, padx=1, pady=1)
                    e.insert(0, "0")
                    row.append(e)
                entries_matrix.append(row)

            conv_block.set_entries_matrix(entries_matrix)

        def apply_preset(*_args):
            """
            Fills any grid size (n > 1) with implemented presets.
            """
            nonlocal entries_matrix
            preset = preset_var.get()

            if not entries_matrix:
                return

            n = len(entries_matrix)

            for row in entries_matrix:
                if len(row) != n:
                    return

            if preset == "Personalizada":
                return

            if preset == "Média":
                value = 1.0 / (n * n)
                for i in range(n):
                    for j in range(n):
                        e = entries_matrix[i][j]
                        e.delete(0, tk.END)
                        e.insert(0, f"{value:.4f}")
                return

            if n < 3:
                return

            for i in range(n):
                for j in range(n):
                    e = entries_matrix[i][j]
                    e.delete(0, tk.END)
                    e.insert(0, "0")

            c = n // 2

            if preset == "Laplaciano (4-vizinhos)":
                entries_matrix[c][c].delete(0, tk.END)
                entries_matrix[c][c].insert(0, "4")

                coords = [
                    (c - 1, c),
                    (c + 1, c),
                    (c, c - 1),
                    (c, c + 1),
                ]
                for i, j in coords:
                    if 0 <= i < n and 0 <= j < n:
                        e = entries_matrix[i][j]
                        e.delete(0, tk.END)
                        e.insert(0, "-1")

            elif preset == "Laplaciano (8-vizinhos)":
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        i = c + di
                        j = c + dj
                        if 0 <= i < n and 0 <= j < n:
                            e = entries_matrix[i][j]
                            e.delete(0, tk.END)
                            if di == 0 and dj == 0:
                                e.insert(0, "8")
                            else:
                                e.insert(0, "-1")

        build_grid()

        size_var.trace_add("write", lambda *args: build_grid())
        preset_var.trace_add("write", lambda *args: apply_preset())

    def _add_difference_block(self) -> None:
        """
        Adds a difference block to the end of the pipeline.
        A diferença é feita entre a imagem atual do pipeline
        e uma outra imagem RAW escolhida no próprio bloco.
        """

        frame = tk.Frame(self._blocks_frame, bd=1, relief="solid", pady=2)
        frame.pack(fill="x", padx=2, pady=2)

        # título do bloco
        tk.Label(frame, text="Diferença com outra imagem RAW").pack(
            side="top", anchor="w"
        )

        # linha de seleção de arquivo
        file_frame = tk.Frame(frame)
        file_frame.pack(fill="x", pady=1)

        tk.Label(file_frame, text="Arquivo:").pack(side="left")

        path_var = tk.StringVar()
        tk.Entry(file_frame, textvariable=path_var, width=30).pack(
            side="left", padx=2
        )

        def browse_other_file():
            path = filedialog.askopenfilename(
                filetypes=[("RAW files", "*.raw"), ("Todos os arquivos", "*.*")]
            )
            if path:
                path_var.set(path)

        tk.Button(file_frame, text="Procurar...", command=browse_other_file).pack(
            side="left", padx=2
        )

        # linha de largura/altura
        size_frame = tk.Frame(frame)
        size_frame.pack(fill="x", pady=1)

        tk.Label(size_frame, text="Largura:").pack(side="left")
        width_var = tk.StringVar()
        tk.Entry(size_frame, textvariable=width_var, width=6).pack(
            side="left", padx=2
        )

        tk.Label(size_frame, text="Altura:").pack(side="left")
        height_var = tk.StringVar()
        tk.Entry(size_frame, textvariable=height_var, width=6).pack(
            side="left", padx=2
        )

        # cria o bloco lógico e adiciona na lista do pipeline
        block = blocks.DifferenceBlock(path_var, width_var, height_var)
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

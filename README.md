# Processamento e Análise de Imagens - Trabalho Prático
Este repositório contém a implementação técnica do trabálho Pratico de *Processamento e Análise de Imagens*.

---

# ✅ Requisitos

- **Python 3.12 ou superior**
- Sistema operacional Windows (para usar o `ExecutarProjeto.bat` diretamente)
- Conexão com a internet apenas na primeira execução (para instalar os pacotes, se necessário)

### **Dependências**:
- MatPlotLib
- Numpy
- Pillow

---

## 🚀 Como executar o projeto (modo recomendado – Windows)

1. Baixe ou clone este repositório:
   - via Git:  
     ```bash
     git clone https://github.com/Iskeletu/PAI---Trabalho-Pr-tico.git
     ```
   - ou faça download do `.zip` pelo GitHub e extraia em uma pasta.

2. Certifique-se de que o **Python 3.12+** está instalado e acessível no PATH.

3. Na pasta do projeto, execute o arquivo **`ExecutarProjeto.bat`**.

    Na primeira execução, ele vai instalar automaticamente os módulos listados em `requirements.txt` e, em seguida, abrir a interface gráfica do projeto.

    Nas próximas vezes, basta rodar o `ExecutarProjeto.bat` de novo, se os módulos já estiverem instalados, o pip só vai confirmar e seguir.

---

## 💻 Execução manual alternativa (sem o .bat)

Se preferir rodar manualmente:
1. Nageve até o diretóio raioz do projeto (onde este arquivo está localizado):
    ```bash
    cd [caminho_para_diretório]
    ```

2. No diretório raiz do projeto, instale as dependências:  
    ```bash
    pip install -r requirements.txt
    ```

3. Depois, execute o script principal:
    ```bash
    python ./src/script.py
    ```

---

## 🧭 Como utilizar o projeto (GUI do PSE-Image)

Depois que o programa abrir, a interface principal permite montar um fluxo de blocos de processamento de imagem. O uso básico é:

### **1. Selecionar a imagem RAW de entrada**

1. Na parte superior, em **“Arquivo RAW”**, clique em **“Procurar…”** e selecione um arquivo `.raw` (8 bits, escala de cinza).

2. Informe a **Largura** e **Altura** da imagem:
    * Se você usou o conversor do próprio projeto, normalmente será algo como `640` × `360`.

3. Esses valores são usados para reconstruir a imagem a partir dos bytes do arquivo.

### **2. Montar o fluxo de blocos**

Na seção “Blocos de processamento (em sequência)”, você pode ir adicionando blocos na ordem desejada. Alguns blocos disponíveis:

* **Adicionar brilho**  
    Aplica um ajuste de brilho pontual.
    * Parâmetro: `Δ`
    * Valor positivo → clareia a imagem
    * Valor negativo → escurece

* **Adicionar limiarização**  
    Aplica uma binarização simples.
    * Parâmetro: `T` (limiar)
    * Pixels abaixo de `T` → 0
    * Pixels acima de `T` → 255 (ou valor máximo)

* **Adicionar convolução**  
    Aplica uma convolução local com máscara parametrizável.
    * Você escolhe o **tamanho da máscara** (3×3, 5×5, 7×7, …).
    * Preenche manualmente os pesos da máscara.
    * Pode usar **presets**:
        * Média (filtro da média);
        * Laplaciano (4-vizinhos);
        * Laplaciano (8-vizinhos).

* **Adicionar histograma**  
    Plota o histograma da imagem no ponto em que o bloco é executado.
    * Não altera a imagem, apenas mostra o gráfico.

* **Adicionar diferença**  
    Calcula a diferença entre a imagem atual do pipeline e outra imagem RAW:
    * Dentro do bloco, você escolhe um segundo arquivo `.raw` e informa largura/altura;
    * As duas imagens precisam ter o **mesmo tamanho**;
    * O bloco gera uma nova imagem de diferença (por exemplo, |img1 − img2|).

* **Adicionar exibição**  
    Mostra a imagem no ponto em que o bloco é executado:
    * Você pode dar um nome/título para a janela (ex.: “Após convolução Laplaciana”);
    * Não altera a imagem, apenas exibe.

* **Adicionar gravação RAW**  
    Salva a imagem naquele ponto do fluxo em um arquivo `.raw`:
    * Você escolhe o caminho e o nome do arquivo de saída;
    * A imagem é gravada em 8 bits, escala de cinza, sem cabeçalho.

Você pode adicionar quantos blocos quiser, eles serão executados de cima para baixo, na ordem em que aparecem na lista.

### **3. Executar o fluxo**

1. Depois de montar o pipeline, clique em **“Processar fluxo”**.

2. O sistema:
    * Lê a imagem RAW de entrada;
    * Executa cada bloco na sequência;
    * Exibe a **Imagem Inicial** e a **Imagem Final**;
    * Executa os blocos de histograma, exibição e gravação nos pontos configurados.

Se houver algum erro (dimensões erradas, arquivo não encontrado, etc.), uma janela de mensagem (messagebox) é mostrada explicando o problema.

4. Redefinir o PSE
    * Para limpar o fluxo e voltar ao estado inicial, clique em **“Redefinir”**.
    * Isso recria a interface, zera a lista de blocos e limpa os campos do arquivo RAW e dimensões.

---

## 🧩 Resumo do que o PSE-Image faz

- Leitura e gravação de imagens RAW (8 bits, escala de cinza);

- Montagem de um fluxo de blocos (brilho, limiarização, convolução, histograma, diferença entre imagens, exibição e gravação);

- Parametrização de cada bloco diretamente pela interface (sem programação textual);

- Visualização da imagem em diferentes etapas do processamento.

---
## 🧩 Estrutura do Projeto
```bash
PAI---Trabalho-Pr-tico/
├── input/                 # Imagens e arquivos RAW de teste (dados de entrada)
├── src/                   # Código-fonte principal do projeto
│   ├── script.py          # Script de entrada da aplicação (inicia o projeto)
│   ├── convert_to_raw.py  # Script de conversão de imagens "normais" (PNG/JPG) para RAW 8 bits, escala de cinza
│   ├── constants.py       # Módulo de definição de constantes globais 
│   ├── PSE/
│   │   ├── problem_solving_environment.py
│   │   │   # Implementação da interface gráfica (Tkinter) do PSE:
│   │   │   #  - Classe PSE_GUI
│   │   │   #  - Criação de blocos e do pipeline
│   │   ├── blocks.py
│   │   │   # Implementação dos blocos de processamento:
│   │   │   #  - BrightnessBlock (brilho)
│   │   │   #  - ThresholdBlock (limiarização)
│   │   │   #  - ConvolutionBlock (convolução local parametrizável)
│   │   │   #  - HistogramBlock (plot de histograma)
│   │   │   #  - DifferenceBlock (diferença entre imagens)
│   │   │   #  - DisplayBlock (exibição em qualquer ponto do fluxo)
│   │   │   #  - SaveRawBlock (gravação de RAW em qualquer ponto)
│   │   └── image_display.py
│   │       # Funções auxiliares para exibir imagens e histogramas
│   │       # (tipicamente usando matplotlib / Pillow)
│   └── FileHandling/
│       └── image_reading.py
│           # Classe RawImageReader: lê imagens RAW 8 bits (sem cabeçalho)
├── ExecutarProjeto.bat    # Script de execução rápido do projeto (instala dependencias e executa script Python primário)
├── requirements.txt       # Lista de dependências Python do projeto
├── config.ini             # Arquivo de configuração (parâmetros gerais) [Não implementado]
├── README.md              # Este arquivo
└── LICENSE                # Licença MIT

```

---

## ✉️ Autor
**Fábio Gandini**  
**Disciplina:** *Processamento e Análise de Imagens – 2025*  
**Instituição:** *Pontifícia Universidade Católica de Minas Gerais*

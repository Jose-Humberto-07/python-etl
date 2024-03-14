import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os

def dividir_e_exportar():
    # Selecionar o arquivo CSV
    arquivo_csv = filedialog.askopenfilename(filetypes=[("Arquivos TXT", "*.txt")])
    if not arquivo_csv:
        return  # Sai se nenhum arquivo for selecionado
    
    # Carregar o arquivo CSV
    df = pd.read_csv(arquivo_csv, sep=";", header=None, names=["te", "aluno", "question"])

    # Dividir os caracteres da coluna "question" em colunas separadas
    df_letras = df["question"].apply(list).apply(pd.Series)
    df_letras = df_letras.add_prefix('')

    # Adicionar 1 ao índice das colunas
    df_letras.columns = range(1, len(df_letras.columns) + 1)

    # Concatenar os DataFrames
    df = pd.concat([df, df_letras], axis=1)

    # Remover a coluna "question"
    df.drop(columns=["question"], inplace=True)

   # Salvar como Excel temporário
    arquivo_saida = "temp.xlsx"
    df.to_excel(arquivo_saida, index=False)

    # Abrir o arquivo Excel
    os.startfile(arquivo_saida)

    messagebox.showinfo("Concluído", "Ação concluída com sucesso!")

    # Remover o arquivo temporário após a execução
    os.remove(arquivo_saida)

# Criar a janela principal
root = tk.Tk()
root.title("Leitor de Gabarito")

# Definir o tamanho da janela
root.geometry("400x200")

# Definir a cor de fundo da janela em hex
root.configure(bg="white")

# Criar o botão
fonte_botao = ("Helvetica", 15)  # Define a fonte do botão
botao_executar = tk.Button(root, text="Gabarito", width=10, height=2, bg="#d3d3d3", fg="black", font=fonte_botao, command=dividir_e_exportar)
botao_executar.pack(pady=60)

# Iniciar a interface
root.mainloop()

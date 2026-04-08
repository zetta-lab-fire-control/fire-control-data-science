"""
utils.py
-----------
Módulo de utilitários para workflow de ciência de dados.
Inclui: 
    - Arquivo entrada/saida
    - auxiliadores de dataframe
    - plotting, logging, timers, e utilitários comuns de préprocessamento.
"""

import zipfile
from typing import Optional, Union
import time
import basedosdados as bd
import os
import shutil
import requests
from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
import sys

current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
import config_path          # Módulo que salva todos os caminhos de diretórios utilizados no projeto

# -------------------------
#  Auxiliador de manipulação de requisição HTTP
# -------------------------
def download_file(url: str, file_name : str, save_path: Path = config_path.RAW_DATA_DIRECTORY_PATH):
    """
    Baixa o arquivo do URL e o salva no caminho local

    Args:
        url (str): URL do arquivo a ser baixado
        file_name (str): Nome do arquivo
        save_path (Path | str): Caminho onde o arquivo será salvo.
    
    Returns:
        Path do arquivo salvo
    """

    # Fazer requisição
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Acionar o erro se o download falhar

    # Salvar conteudo do arquivo localmente
    with open(f"{save_path}/{file_name}", 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Arquivo baixado e salvo em: {save_path}/{file_name}")
    return Path(save_path) / file_name

def check_contained_files_zip(zip_file_path: Path) -> list[str]:
    """
    Retorna uma lista de arquivos contido no ZIP
    
    Args:
        zip_file_path (Path): Caminho completo do arquivo ZIP.
    Returns:
        extracted_files (list[str]): Lista de arquivos contido no ZIP.
    """
    
    if not zip_file_path.exists():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não existe")
    
    if not zip_file_path.is_file():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não é um arquivo")
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        extracted_files = zip_ref.namelist()
    
    return extracted_files

# -----------------------------------
#  Descompactar arquivo Zip
# -----------------------------------
def unzip_and_clean(zip_file_path: Path, files_to_keep: Optional[list[str]] | str | None = 'all', extract_path: Path = config_path.RAW_DATA_DIRECTORY_PATH):
    """
    Descompacta um arquivo ZIP e remove todos os arquivos que você não quer

    Args:
        zip_file_path (Path): Caminho completo para salvar o ZIP (ex: "C:/temp/meuarquivo.zip").
        files_to_keep (list[str] str | None): Nome do arquivo que queremos manter (ex: "importante.txt").
        extract_path (Path | str): Caminho do diretório em que o arquivo ZIP está localizado.
    Returns:
        kept_paths (list): Lista de caminhos dos arquivos mantidos.
    """
    
    if isinstance(files_to_keep, list) and len(files_to_keep) <= 0:
        raise ValueError(f"ERRO: Argumento 'files_to_keep' não possui tamanho maior que zero!")
    
    if not zip_file_path.exists():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não existe")
    
    if not zip_file_path.is_file():
        raise FileNotFoundError(f"ERRO: '{zip_file_path}' não é um arquivo")
        
    # 1. Extrair todo o conteúdo
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        extracted_files = zip_ref.namelist()
        
    print(f"Arquivos extraídos em: {extract_path}")

    # 2. Percorrer todos os arquivos e remover os indesejados
    kept_paths = []
    
    if files_to_keep == 'all' or files_to_keep is None:
        kept_paths = [Path(extract_path) / f for f in extracted_files if not f.endswith('/')]  # só arquivos
        print(f"Arquivos mantidos: {kept_paths}")
        
        try:
            zip_file_path.unlink()
            print(f"ZIP removido: {zip_file_path}")
        except Exception as e:
            print(f"ERRO ao remover ZIP: {e}")
        
        return kept_paths
    
    for file in extracted_files:
        file_path = Path(extract_path) / file

        # ignora diretórios
        if file_path.is_dir():
            continue

        file_name = file_path.name

        if file_name in files_to_keep:
            kept_paths.append(file_path)
        else:
            file_path.unlink()
            print(f"Removido: {file_path}")
    
    
    try:
        zip_file_path.unlink()
        print(f"ZIP removido: {zip_file_path}")
    except Exception as e:
        print(f"ERRO ao remover ZIP: {e}")
    
    # 3. Retornar os arquivos que foram mantidos
    print(f"Arquivos mantidos: {kept_paths}")
    return kept_paths

# -----------------------------
# Auxiliadores de Dataframe
# -----------------------------
def describe_df(df: pd.DataFrame):
    """
    Imprime as informações, shape e descrição de um DataFrame
    """
    print(f"Shape: {df.shape}\n")
    print("Info:")
    print(df.info())
    print("\nDescription:")
    print(df.describe())

def missing_summary(df: pd.DataFrame):
    """
    Retorna os valores nulos e porcentagem por coluna
    """
    total = df.isnull().sum()
    percent = (total / len(df)) * 100
    return pd.DataFrame({'missing': total, 'percent': percent}).sort_values('percent', ascending=False)

# -----------------------------
# Auxiliadores de plotting
# -----------------------------
from pathlib import Path
from typing import Optional, Union
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_pie_chart(
    data: Union[list, pd.Series, np.ndarray],
    labels: Union[list, pd.Series, np.ndarray],
    title: str,
    palette: str = 'Set2',
    ax=None,
    path_file: Optional[Path] = None,
    figsize: tuple[int, int] = (8, 8),
    autopct: str = '%1.1f%%',
    startangle: int = 90,
    explode: Optional[list[float]] = None,
    legend_outside: bool = True
):
    """
    Cria um pie chart profissional e reutilizável com Seaborn.

    Args:
        data (list, Series, np.ndarray): Tamanho de cada fatia.
        labels (list, Series, np.ndarray): Labels de cada fatia.
        title (str): Título do gráfico.
        palette (str): Paleta de cores do Seaborn.
        ax (matplotlib.axes.Axes, opcional): Eixo para plotar. Se None, cria figura nova.
        path_file (Path, opcional): Caminho para salvar a figura.
        figsize (tuple, opcional): Tamanho da figura.
        autopct (str, opcional): Formato do percentual das fatias.
        startangle (int, opcional): Ângulo inicial do gráfico.
        explode (list[float], opcional): Distância de cada fatia para “explodir”.
        legend_outside (bool, opcional): Coloca legenda fora do gráfico.
    """
    # Converter para lista
    if isinstance(data, (pd.Series, np.ndarray)):
        data = data.tolist()
    if isinstance(labels, (pd.Series, np.ndarray)):
        labels = labels.tolist()

    # Criar figura se necessário
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        fig_created = True
    else:
        fig_created = False

    # Explode padrão se não definido
    if explode is None:
        explode = [0] * len(data)

    # Cores automáticas do Seaborn
    colors = sns.color_palette(palette, len(data))

    # Plot
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels if not legend_outside else None,
        colors=colors,
        autopct=autopct,
        startangle=startangle,
        explode=explode
    )
    ax.axis('equal')
    ax.set_title(title)

    # Legenda fora do gráfico
    if legend_outside:
        ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5))

    # Salvar ou mostrar
    if path_file:
        plt.savefig(path_file, bbox_inches='tight')
        if fig_created:
            plt.close()
    else:
        plt.show()

def plot_bar_chart(
    data: Union[list, pd.Series, np.ndarray],
    labels: Union[list, pd.Series, np.ndarray],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    orientation: str = 'vertical',  # 'vertical' ou 'horizontal'
    palette: str = 'Set2',
    figsize: tuple[int,int] = (10,6),
    show_values: bool = True,
    value_format: str = '.1f',
    sort: Optional[str] = 'desc',   # 'asc', 'desc', ou None
    ax=None,
    path_file: Optional[Path] = None
):
    """
    Cria um bar chart reutilizável e flexível.

    Args:
        data (list, Series ou np.ndarray): Valores das barras.
        labels (list, Series ou np.ndarray): Labels correspondentes.
        title (str): Título do gráfico.
        xlabel (str): Label do eixo X.
        ylabel (str): Label do eixo Y.
        orientation (str): 'vertical' ou 'horizontal'.
        palette (str): Paleta de cores do Seaborn.
        figsize (tuple): Tamanho da figura.
        show_values (bool): Mostrar valores nas barras.
        value_format (str): Formato dos valores (ex: '.1f').
        sort (str ou None): Ordenar 'asc', 'desc' ou None.
        ax (matplotlib.axes.Axes): Eixo para plotar. Se None, cria figura nova.
        path_file (Path, opcional): Caminho para salvar o gráfico.
    """
    # Converter para lista
    if isinstance(data, (pd.Series, np.ndarray)):
        data = data.tolist()
    if isinstance(labels, (pd.Series, np.ndarray)):
        labels = labels.tolist()
    
    # Ordenar se necessário
    if sort in ['asc','desc']:
        combined = sorted(zip(labels, data), key=lambda x: x[1], reverse=(sort=='desc'))
        labels, data = zip(*combined)
    
    # Criar figura se necessário
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        fig_created = True
    else:
        fig_created = False
    
    # Cores
    colors = sns.color_palette(palette, len(data))
    
    # Plot
    if orientation == 'vertical':
        bars = ax.bar(labels, data, color=colors)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    else:
        bars = ax.barh(labels, data, color=colors)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    
    ax.set_title(title)
    
    # Mostrar valores nas barras
    if show_values:
        for bar in bars:
            if orientation == 'vertical':
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height, f"{height:{value_format}}", 
                        ha='center', va='bottom', fontsize=10)
            else:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2, f"{width:{value_format}}", 
                        ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    
    # Salvar ou mostrar
    if path_file:
        plt.savefig(path_file, bbox_inches='tight')
        if fig_created:
            plt.close()
    else:
        plt.show()

def plot_heatmap(
    df: pd.DataFrame,
    values: str,
    index: str,
    columns: str,
    aggfunc: str = 'sum',
    cmap: str = "YlOrRd",
    annot: bool = True,
    fmt: str = ".1f",
    figsize: tuple[int,int] = (12,8),
    title: Optional[str] = None,
    path_file: Optional[Path] = None
):
    """
    Cria um heatmap flexível a partir de um DataFrame.

    Args:
        df (pd.DataFrame): DataFrame de origem.
        values (str): Coluna numérica a ser agregada (ex: 'Área queimada (ha)').
        index (str): Coluna que será usada como eixo Y.
        columns (str): Coluna que será usada como eixo X.
        aggfunc (str, opcional): Função de agregação ('sum', 'mean', etc.).
        cmap (str, opcional): Paleta de cores do Seaborn.
        annot (bool, opcional): Mostrar os valores dentro das células.
        fmt (str, opcional): Formato dos valores (ex: '.1f').
        figsize (tuple, opcional): Tamanho da figura.
        title (str, opcional): Título do gráfico.
        path_file (Path, opcional): Caminho para salvar o gráfico.
    """
    # Criar pivot table
    pivot_table = pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc=aggfunc)
    
    # Criar figura
    plt.figure(figsize=figsize)
    sns.heatmap(pivot_table, cmap=cmap, annot=annot, fmt=fmt, cbar_kws={'label': values})
    
    plt.xlabel(columns)
    plt.ylabel(index)
    if title:
        plt.title(title)
    
    plt.tight_layout()
    
    # Salvar ou mostrar
    if path_file:
        plt.savefig(path_file, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_histogram(df: pd.DataFrame, col: list[str], bins: int = 30, figsize: Tuple[int, int] = (10, 6)):
    plt.figure(figsize=figsize)
    
    # Adicionando o KDE para ver a "forma" da distribuição
    ax = sns.histplot(df[col], bins=bins, kde=True, color='skyblue', edgecolor='black')
    
    # Adicionando linhas de média e mediana
    mean = df[col].mean()
    median = df[col].median()
    
    plt.axvline(mean, color='red', linestyle='--', label=f'Média: {mean:.2f}')
    plt.axvline(median, color='green', linestyle='-', label=f'Mediana: {median:.2f}')
    
    plt.title(f'Distribuição de {col}', fontsize=15)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

def plot_correlation(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 10)):
    # Calcular apenas para colunas numéricas para evitar erros
    corr = df.select_dtypes(include=[np.number]).corr()
    
    # Criar uma máscara para esconder o triângulo superior (repetido)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    plt.figure(figsize=figsize)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='RdBu_r', 
                center=0, square=True, linewidths=.5, cbar_kws={"shrink": .8})
    
    plt.title('Matriz de Correlação (Triângulo Inferior)', fontsize=15)
    plt.show()

def plot_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue: Optional[str] = None,
    size: Optional[str] = None,
    regression: bool = True,
    log_x: bool = False,
    log_y: bool = False,
    palette: str = 'Set2',
    figsize: tuple[int,int] = (8,8),
    marginal_bins: int = 20,
    marginal_fill: bool = True,
    show_corr: bool = True,
    title: Optional[str] = None,
    path_file: Optional[Union[str, Path]] = None
):
    """
    Cria scatter plot flexível com histogramas marginais e regressão opcional.

    Args:
        df (pd.DataFrame): DataFrame de origem.
        x_col (str): Nome da coluna para eixo X.
        y_col (str): Nome da coluna para eixo Y.
        hue (str, opcional): Coluna para colorir os pontos.
        size (str, opcional): Coluna para definir tamanho dos pontos.
        regression (bool, opcional): Se True, adiciona linha de regressão.
        log_x (bool, opcional): Aplica escala logarítmica no eixo X.
        log_y (bool, opcional): Aplica escala logarítmica no eixo Y.
        palette (str, opcional): Paleta de cores do Seaborn.
        figsize (tuple, opcional): Tamanho da figura.
        marginal_bins (int, opcional): Número de bins nos histogramas marginais.
        marginal_fill (bool, opcional): Preenchimento dos histogramas marginais.
        show_corr (bool, opcional): Mostra correlação de Pearson.
        title (str, opcional): Título do gráfico.
        path_file (str | Path, opcional): Caminho para salvar o gráfico.
    """
    
    kind = "reg" if regression else "scatter"
    
    # Configurar estilo
    sns.set(style="whitegrid")
    
    # Jointplot com histogramas marginais
    g = sns.jointplot(
        data=df,
        x=x_col,
        y=y_col,
        hue=hue,
        size=size,
        kind=kind,
        palette=palette,
        height=figsize[0],
        ratio=5,
        marginal_kws=dict(bins=marginal_bins, fill=marginal_fill)
    )
    
    # Escala logarítmica
    if log_x:
        g.ax_joint.set_xscale('log')
    if log_y:
        g.ax_joint.set_yscale('log')
    
    # Título
    if title is None:
        title = f'Relação: {x_col} vs {y_col}'
    g.figure.suptitle(title, y=1.02, fontsize=15)
    
    # Correlação
    if show_corr and not regression:
        corr_coef, p_val = pearsonr(df[x_col], df[y_col])
        g.ax_joint.text(0.05, 0.95, f'r = {corr_coef:.2f}', transform=g.ax_joint.transAxes,
                        fontsize=12, verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5))
    
    plt.tight_layout()
    
    # Salvar ou mostrar
    if path_file:
        plt.savefig(path_file, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

# -----------------------------
# Auxiliadores de logging e timer
# -----------------------------
def log(message: str):
    """Simple logger."""
    print(f"[INFO] {message}")

def timer(func):
    """Decorator to time function execution."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} executed in {end-start:.2f} seconds")
        return result
    return wrapper

# -----------------------------
# Checagem de valores e estado do DataFrame
# -----------------------------
def ensure_columns(df: pd.DataFrame, columns: list[str]):
    """
    Checa se colunas existem no DataFrame, retorna um erro se não possuir
    """
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def unique_values_summary(df: pd.DataFrame, columns: list[str]):
    """
    Retorna o número de valores únicos por coluna especifica
    """
    return {col: df[col].nunique() for col in columns}

def value_counts_summary(df: pd.DataFrame, columns: list[str]):
    """
    Retorna a contagem de valores por múltiplas colunas
    """
    return {col: df[col].value_counts() for col in columns}
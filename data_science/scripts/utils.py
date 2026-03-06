# utils.py
"""
Módulo de utilitários para workflow de ciência de dados.
Inclui: arquivo entrada/saida, auxiliadores de dataframe, plotting, logging, timers, e utilitários comuns de préprocessamento.
"""

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Auxiliadores de escrita e carregamento de arquivos
# -----------------------------
def save_pickle(obj, file_path):
    """Save a Python object to a pickle file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def load_pickle(file_path):
    """Load a Python object from a pickle file."""
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def ensure_dir(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

# -----------------------------
# Auxiliadores de Dataframe
# -----------------------------
def describe_df(df):
    """Print shape, info, and description of a DataFrame."""
    print(f"Shape: {df.shape}\n")
    print("Info:")
    print(df.info())
    print("\nDescription:")
    print(df.describe())

def missing_summary(df):
    """Return missing values count and percentage per column."""
    total = df.isnull().sum()
    percent = (total / len(df)) * 100
    return pd.DataFrame({'missing': total, 'percent': percent}).sort_values('percent', ascending=False)

# -----------------------------
# Auxiliadores de plotting
# -----------------------------
def plot_histogram(df, col, bins=30, figsize=(8,5)):
    plt.figure(figsize=figsize)
    df[col].hist(bins=bins)
    plt.title(f'Histogram of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

def plot_correlation(df, figsize=(10,8)):
    plt.figure(figsize=figsize)
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

def plot_scatter(df, x_col, y_col, hue=None, figsize=(8,6)):
    plt.figure(figsize=figsize)
    sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue)
    plt.title(f'Scatter Plot: {x_col} vs {y_col}')
    plt.show()

# -----------------------------
# Auxiliadores de logging e timer
# -----------------------------
def log(message: str):
    """Simple logger."""
    print(f"[INFO] {message}")

def timer(func):
    """Decorator to time function execution."""
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} executed in {end-start:.2f} seconds")
        return result
    return wrapper

# -----------------------------
# Funções utilitárias
# -----------------------------
def ensure_columns(df: pd.DataFrame, columns: list[str]):
    """Check if columns exist in DataFrame, raise error if missing."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def unique_values_summary(df: pd.DataFrame, columns: list[str]):
    """Return the number of unique values per specified column."""
    return {col: df[col].nunique() for col in columns}

def value_counts_summary(df: pd.DataFrame, columns: list[str]):
    """Return value counts for multiple columns."""
    return {col: df[col].value_counts() for col in columns}
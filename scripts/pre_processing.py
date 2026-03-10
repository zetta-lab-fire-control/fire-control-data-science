"""
pre_processing.py
--------------------
Módulo de funções reutilizáveis para pré-processamento de dados
Inclui:
    - Merge de DataFrames
    - Concatenação de DataFrames
    - Preenchimento de Valores Nulos
    - Entre outros.
"""

import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pathlib import Path

# -----------------------------
# Auxiliadores de pré processamento
# -----------------------------
def remove_blank_rows_cols_csv(caminho_arquivo: str | Path, separador: str = ',') -> pd.DataFrame:
    """
    Lê um arquivo CSV e remove colunas e linhas que não contêm dados úteis.

    Args:
        caminho_arquivo (str): Caminho para o arquivo .csv.
        separador (str): O delimitador do CSV (padrão é vírgula).

    Returns:
        pd.DataFrame: DataFrame limpo e pronto para análise.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado.")
        return pd.DataFrame()

    try:
        # 1. Carrega o CSV (low_memory=False ajuda com datasets grandes e tipos mistos)
        df = pd.read_csv(caminho_arquivo, sep=separador, low_memory=False)
        
        formato_original = df.shape

        # 2. Remove linhas que são TOTALMENTE vazias (NaN)
        df = df.dropna(how='all', axis=0)

        # 3. Remove colunas que são TOTALMENTE vazias (NaN)
        df = df.dropna(how='all', axis=1)

        # 4. Remove colunas "fantasmas" (comuns em CSVs com vírgulas sobrando no final da linha)
        # Filtra colunas que começam com 'Unnamed' e são 100% nulas
        colunas_unnamed_vazias = [
            col for col in df.columns 
            if "Unnamed" in str(col) and df[col].isnull().all()
        ]
        df = df.drop(columns=colunas_unnamed_vazias)

        # 5. Remove espaços em branco dos nomes das colunas
        df.columns = [str(col).strip() for col in df.columns]
        
        return df
    except Exception as e:
        print(f"Erro ao processar o CSV: {e}")
        return pd.DataFrame()

def remove_blank_rows_cols_excel(df: pd.DataFrame, limite_nulos: float = 0.9) -> pd.DataFrame:
    """
    Remove automaticamente linhas e colunas inúteis de um DataFrame vindo do Excel.
    
    Ações:
    1. Remove colunas que são 100% vazias.
    2. Remove linhas que são 100% vazias.
    3. Remove colunas que possuem mais de 'limite_nulos' de valores NaN.
    4. Remove espaços em branco extras nos nomes das colunas.

    Args:
        df (pd.DataFrame): O DataFrame carregado do Excel.
        limite_nulos (float): De 0 a 1. Se 0.9, remove colunas com 90% ou mais de nulos.

    Returns:
        pd.DataFrame: O DataFrame limpo.
    """
    # Copia para não alterar o original por acidente
    df_limpo = df.copy()

    # 1. Remover linhas e colunas que são TOTALMENTE vazias (comum no Excel)
    df_limpo = df_limpo.dropna(how='all', axis=0) # Linhas
    df_limpo = df_limpo.dropna(how='all', axis=1) # Colunas

    # 2. Remover colunas com excesso de nulos (sujeira de formatação)
    # Ex: Uma coluna de "Observações" onde quase ninguém escreveu nada
    df_limpo = df_limpo.loc[:, df_limpo.isnull().mean() < limite_nulos]

    # 3. Limpar os nomes das colunas (Excel costuma ter " Nome Cliente " com espaços)
    df_limpo.columns = [str(col).strip() for col in df_limpo.columns]
    
    # 4. Remover colunas 'Unnamed' (aquelas colunas vazias que o pandas cria)
    colunas_validas = [col for col in df_limpo.columns if "Unnamed" not in col]
    df_limpo = df_limpo[colunas_validas]

    print(f"🧹 Limpeza concluída: {df.shape[1] - df_limpo.shape[1]} colunas removidas.")
    return df_limpo

def concat_dfs(*dfs: pd.DataFrame, axis: int =0, ignore_index: bool = True, join: str ='outer') -> pd.DataFrame:
    """
    Concatena múltiplos DataFrames por linhas ou colunas.
    
    Parameters:
        *dfs (pd.DataFrame): Dois ou mais DataFrames.
        axis (int): 0 para concatenar por linha (padrão), 1 para concatenar por coluna.
        ignore_index (bool): Indica se deve reiniciar o index após a concatenação (padrão True)
        join (str): 'outer' para união, 'inner' para interseção (padrão 'outer')
        
    Returns:
        DataFrame concatenado.
    """
    if len(dfs) <= 1:
        raise ValueError("ERRO: 'concat_dfs' precisa de pelo menos dois DataFrame.")
    
    concatenated_df = pd.concat(dfs, axis=axis, ignore_index=ignore_index, join=join)
    return concatenated_df

def fill_missing(df : pd.DataFrame, strategy : str ='zero') -> pd.DataFrame:
    """
    Preenche valores ausentes (NULL/NaN) em todo o DataFrame.
    
    Esta função aplica uma estratégia única de preenchimento para todas as colunas
    vazias, facilitando a limpeza rápida de dados antes de análises ou modelagem.

    Args:
        df (pd.DataFrame): O DataFrame que contém os valores nulos.
        strategy (str): O método de preenchimento. 
            'zero' (padrão): Substitui por 0.
            'mean': Substitui pela média aritmética da coluna.
            'median': Substitui pela mediana (menos sensível a valores extremos).

    Returns:
        pd.DataFrame: Uma cópia do DataFrame com os valores nulos preenchidos.
    
    Raises:
        ValueError: Se a 'strategy' informada for inválida.
    """
    
    if strategy not in ['zero', 'mean', 'median']:
        raise ValueError(f"ERRO: Método de preenchimento '{strategy}' não suportado. Utilize 'zero','mean', ou 'median'.")
    
    try:
        
        if strategy == 'zero':
            return df.fillna(0)
        elif strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
    except KeyError as e:
        print(f"ERRO: Uma das colunas não foi encontrada: {e}")
        raise
    except TypeError as e:
        print(f"ERRO: Não foi possível calcular a estatística. Verifique se as colunas são numéricas: {e}")
        return df
        

def scale_features(df : pd.DataFrame, columns : list[str], method : str = 'standard') -> pd.DataFrame:
    """
    Realiza o escalonamento de colunas numéricas específicas de um DataFrame.
    
    Esta função gera uma cópia dos dados para evitar alterações no original e 
    aplica a transformação escolhida para normalizar ou padronizar as escalas.
    
    Args:
        df (pd.DataFrame): O DataFrame que contém os dados a serem processados.
        columns (list[str]): Lista com os nomes das colunas que devem ser escalonadas.
        method (str, opcional): O método de escalonamento. 
            'standard': (Padrão) Aplica média 0 e desvio padrão 1.
            'minmax': Redimensiona os dados para o intervalo entre 0 e 1.

    Returns:
        pd.DataFrame: Uma nova instância do DataFrame com as colunas transformadas.

    Raises:
        ValueError: Caso o 'method' informado não seja 'standard' ou 'minmax'.
    """
    if method not in ['standard', 'minmax']:
        raise ValueError(f"ERRO: Método '{method}' não suportado. Use 'standard' ou 'minmax'.")
    
    try:
        df_scaled = df.copy()
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        df_scaled[columns] = scaler.fit_transform(df_scaled[columns])
        return df_scaled
    except KeyError as e:
        print(f"ERRO: Uma das colunas não foi encontrada: {e}")
        raise
    except TypeError:
        print("ERRO: O escalonamento falhou. Verifique se todas as colunas são numéricas.")
        return df

def merge_dfs(df_left : pd.DataFrame, df_right : pd.DataFrame, on: str | None = None, how: str ='left') -> pd.DataFrame:
    """
    Realiza a junção (merge) de dois DataFrames com base em uma coluna comum.

    Esta função facilita a união de tabelas, garantindo que a coluna de 
    ligação seja explicitamente informada para evitar merges automáticos 
    indesejados.

    Args:
        df_left (pd.DataFrame): O DataFrame principal (à esquerda).
        df_right (pd.DataFrame): O DataFrame a ser mesclado (à direita).
        on (str | None): O nome da coluna (chave) que será usada na junção. 
            Deve ser informada obrigatoriamente.
        how (str): O método de junção. Opções: 'left' (padrão), 'right', 'inner', 'outer'.

    Returns:
        pd.DataFrame: O DataFrame resultante da junção.

    Raises:
        ValueError: Se o argumento 'on' não for fornecido.
    """
    if on is None:
        raise Exception("ERRO: O argumento 'on' (coluna de ligação) é obrigatório e não foi informado.")
    
    merged = pd.merge(df_left, df_right, on=on, how=how)
    return merged

def merge_several_dfs(*dfs: pd.DataFrame, on: list[str] | None = None, how: str = 'left') -> pd.DataFrame:
    """
    Realiza a junção (merge) sequencial de múltiplos DataFrames.

    Esta função recebe dois ou mais DataFrames e os une um a um com base 
    nas colunas informadas, mantendo a ordem da sequência fornecida.

    Args:
        *dfs (pd.DataFrame): Dois ou mais DataFrames do Pandas para serem unidos.
        on (list[str] | None): Lista com os nomes das colunas (chaves) para a junção. 
            É obrigatório fornecer este argumento.
        how (str): O método de junção ('left', 'right', 'inner', 'outer'). 
            O padrão é 'left'.

    Returns:
        pd.DataFrame: Um único DataFrame contendo a união de todos os inputs.

    Raises:
        ValueError: Se menos de dois DataFrames forem fornecidos ou se 'on' for None.
    """
    if len(dfs) <= 1:
        raise Exception("ERRO: Função 'merge_several_dfs' necessita de pelo menos dois dataframes para executar.")
    if on is None:
        raise Exception("ERRO: Argumento 'on' não recebeu lista de strings.")
    
    # Começa com o primeiro DataFrame
    merged_df = dfs[0]
    
    # Itera pelos DataFrames restantes e faz o merge sequencial
    for df in dfs[1:]:
        merge_df = pd.merge(merge_df, df, on=on, how=how)
    
    return merged_df
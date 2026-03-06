import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pathlib import Path

# -----------------------------
# Auxiliadores de pré processamento
# -----------------------------
def download_file(url: str, file_name : str, save_path: Path):
    """
    Download a file from a URL and save it to a local path.

    Parameters:
        url: The URL of the file to download.
        save_path: The local path where the file will be saved.
    """

    # Make the request
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise error if the download failed

    # Write content to file
    with open(f"{save_path}/{file_name}", 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"File downloaded and saved to: {save_path}/{file_name}")

def concat_dfs(*dfs: pd.DataFrame, axis: int =0, ignore_index: bool = True, join: str ='outer'):
    """
    Concatenate multiple DataFrames along rows or columns.
    
    Parameters:
        *dfs: Two or more pandas DataFrames
        axis: 0 to concatenate rows (default), 1 to concatenate columns
        ignore_index: Whether to reset the index after concatenation (default True)
        join: 'outer' for union of columns, 'inner' for intersection (default 'outer')
        
    Returns:
        Concatenated DataFrame
    """
    if len(dfs) == 0:
        raise ValueError("ERRO: 'concat_dfs' precisa de pelo menos um DataFrame.")
    
    concatenated_df = pd.concat(dfs, axis=axis, ignore_index=ignore_index, join=join)
    return concatenated_df

def fill_missing(df : pd.DataFrame, strategy : str ='zero'):
    """Fill missing values in a DataFrame."""
    if strategy == 'zero':
        return df.fillna(0)
    elif strategy == 'mean':
        return df.fillna(df.mean())
    elif strategy == 'median':
        return df.fillna(df.median())
    return df

def scale_features(df : pd.DataFrame, columns : list[str], method : str = 'standard'):
    """Scale numeric features using StandardScaler or MinMaxScaler."""
    df_scaled = df.copy()
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    else:
        raise ValueError("method must be 'standard' or 'minmax'")
    df_scaled[columns] = scaler.fit_transform(df_scaled[columns])
    return df_scaled

def merge_dfs(df_left : pd.DataFrame, df_right : pd.DataFrame, on: str | None = None, how: str ='left'):
    """
    Merge one DataFrame with another get the result.
    
    Parameters:
        df_left: DataFrame on the left
        df_right: Dataframe on the right
        on: Column name(s) to merge on. Default is None.
        how: Merge method ('left', 'right', 'inner', 'outer'). Default is 'left'.
    
    Returns:
        Merged DataFrame
    """
    if on is None:
        raise Exception("ERRO: Argumento 'on' não recebeu lista de strings.")
    
    merged = pd.merge(df_left, df_right, on=on, how=how)
    return merged

def merge_several_dfs(*dfs: pd.DataFrame, on: list[str] | None = None, how: str ='left'):
    """
    Merge several DataFrames in sequence and return the result.
    
    Parameters:
        *dfs: Two or more pandas DataFrames
        on: Column name(s) to merge on. Default is None.
        how: Merge method ('left', 'right', 'inner', 'outer'). Default is 'left'.
    
    Returns:
        Merged DataFrame
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
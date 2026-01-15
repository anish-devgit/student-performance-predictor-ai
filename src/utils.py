import pandas as pd
import os

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads a CSV file into a Pandas DataFrame.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
        print(f"Successfully loaded data from {filepath}")
        print(f"Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def get_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a summary DataFrame with column names, types, missing values, and unique counts.
    """
    info = pd.DataFrame({
        'Type': df.dtypes,
        'Missing': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df)) * 100,
        'Unique': df.nunique(),
        'Example': df.iloc[0] if not df.empty else None
    })
    return info

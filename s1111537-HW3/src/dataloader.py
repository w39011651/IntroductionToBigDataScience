import pandas as pd
from constant import filePath
import os

def load_data(file_path:str)->pd.DataFrame:
    return pd.read_csv(file_path)

import matplotlib.pyplot as plt
import dataprocessor, dataloader, constant
import seaborn as sns
from typing import List, Dict
import numpy as np


def plot_era_histogram(era_lists, bins=20):
    # 合併所有年份的ERA
    rounded_era = [round(float(x), 3) for x in era_lists]
    # 畫勝率最高球隊
    plt.figure(figsize=(10,5))
    sns.histplot(rounded_era, bins=bins, kde=True)
    plt.title("The Highest winrate pitcher's ERA Distribution")
    plt.xlabel("ERA")
    plt.ylabel("Number of pitcher")
    plt.xlim(min(rounded_era), max(rounded_era))  # 強制X軸範圍
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
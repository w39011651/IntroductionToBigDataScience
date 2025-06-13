import pandas as pd
from typing import Dict, List, Tuple
import dataloader, constant
import numpy as np
import json


def find_top_bottom_teams_by_year(team_df:pd.DataFrame) -> Dict[int, Dict[str, str]]:
    """
    找出每年勝率最高與最低的球隊 ID。

    Args:
        team_df (pd.DataFrame): 包含所有年份的球隊數據。
                                需要有 'year', 'team_id', 'win_percentage' 欄位。

    Returns:
        A dictionary mapping year to best/worst team IDs.
        Example: {2023: {'best_team': 'T1', 'worst_team': 'T5'}}
    """
    team_df['win_percentage'] = team_df['W'] / (team_df['W'] + team_df['L'])

    idx_max = team_df.groupby('Year')['win_percentage'].idxmax()
    idx_min = team_df.groupby('Year')['win_percentage'].idxmin()

    best_teams = team_df.loc[idx_max, ['Year', 'TEAM']]
    worst_teams = team_df.loc[idx_min, ['Year', 'TEAM']]

    result = {}
    for year in range(2003, 2024):
        best_team = best_teams[best_teams['Year'] == year]['TEAM'].values[0]
        worst_team = worst_teams[worst_teams['Year'] == year]['TEAM'].values[0]
        result[year] = {'best_team':best_team, 'worst_team':worst_team}

    return result

def mapping_abbr(pitcher_df:pd.DataFrame):
    with open(constant.filePath.ABBR_PATH.value, 'r') as f:
        get_name_by_abbr = json.load(f)
    pitcher_df['TEAM_FULL_NAME'] = pitcher_df['TEAM'].map(get_name_by_abbr)

def get_pitcher_era(pitcher_df:pd.DataFrame, team_map:Dict[int, Dict[str, str]])->Dict[int, Dict[str, List]]:
    results = {}
    for k,v in team_map.items():
        best_list = pitcher_df[(pitcher_df['Year'] == k) & (pitcher_df['TEAM_FULL_NAME'] == v['best_team'])]['ERA']
        worst_list = pitcher_df[(pitcher_df['Year'] == k) & (pitcher_df['TEAM_FULL_NAME'] == v['worst_team'])]['ERA']

        results[k] = {"best_teams_number_of_pichers":best_list, "worst_teams_number_of_pichers":worst_list}
    return results

def get_era_by_team(df:pd.DataFrame, team_map:Dict[int, Dict[str, str]])->Tuple[List, List]:
    results = {}
    total_best_list = []
    total_worst_list = []
    for k,v in team_map.items():
        best_era = df[(df['Year'] == k) & (df['TEAM_FULL_NAME'] == v['best_team']) & (df['ERA'] != '-.--')]['ERA']
        worst_era = df[(df['Year'] == k) & (df['TEAM_FULL_NAME'] == v['worst_team']) & (df['ERA'] != '-.--')]['ERA']
        
        #results[k] = {"best_team_era": best_era, "worst_team_era": worst_era}
        total_best_list.extend(best_era)
        total_worst_list.extend(worst_era)

    return (total_best_list, total_worst_list)

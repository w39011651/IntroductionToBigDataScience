import openpyxl
import csv

def save_to_player_csv(std_label, exp_label, total_data):
    with open("player.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year'] + std_label + exp_label[2:])
        for idx, each_year_data in enumerate(total_data):
            for player, data in each_year_data.items():
                row = [str(2003+idx),player]+data['Standard']+data['Expanded'][1:]
                writer.writerow(row)

        print("Save data done.")

"""
[outter p
    {year1
        player1: {std:data, exp:data},
        player2: {std:data, exp:data},
        .
        .
        .
    },
    {year2
        .
        .
        .
    },
    .
    .
    .
]
"""

def save_to_team_csv(std_label, exp_label, total_data):
    with open("team.csv", "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year'] + std_label + exp_label[2:])
        for idx, each_year_data in enumerate(total_data):
            for player, data in each_year_data.items():
                row = [str(2003+idx),player]+data['Standard']+data['Expanded'][1:]
                writer.writerow(row)

        print("Save data done.")

"""
[
    {year1
        TEAM1: {std:data, exp:data},
        TEAM2: {std:data, exp:data},
        .
        .
        .
    },
    {year2
        .
        .
        .
    },
    .
    .
    .
]
"""
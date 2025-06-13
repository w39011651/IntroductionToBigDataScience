import sqlite3
import pandas as pd
import json
from tqdm import tqdm

abbr_to_name = None

def connect_to_db():
    conn = sqlite3.connect("db/mlb.db")
    cursor = conn.cursor()
    return conn, cursor

def create_tables(conn:sqlite3.Connection, cursor:sqlite3.Cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Season (
                SeasonID INTEGER PRIMARY KEY,
                SeasonYear INTEGER NOT NULL
                );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Player (
                   PlayerID INTEGER PRIMARY KEY,
                   Name TEXT NOT NULL
                   );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Team (
                   TeamID INTEGER PRIMARY KEY,
                   TeamName TEXT NOT NULL,
                   League TEXT NOT NULL
                   );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PitchingStats (
                    StatsID INTEGER PRIMARY KEY,
                    SeasonID INTEGER,
                    PlayerID INTEGER,
                    TeamID INTEGER,
                    "W" INTEGER,
                    "L" INTEGER,
                    "ERA" DOUBLE,
                    "G" INTEGER,
                    "GS" INTEGER,
                    "CG" INTEGER,
                    "SHO" INTEGER,
                    "SV" INTEGER,
                    "SVO" INTEGER,
                    "IP" DOUBLE,
                    "H" INTEGER,
                    "R" INTEGER,
                    "ER" INTEGER,
                    "HR" INTEGER,
                    "HB" INTEGER,
                    "BB" INTEGER,
                    "SO" INTEGER,
                    "WHIP" DOUBLE,
                    "AVG" DOUBLE,
                    "TBF" INTEGER,
                    "NP" INTEGER,
                    "PIP" DOUBLE,
                    "QS" INTEGER,
                    "GF" INTEGER,
                    "HLD" INTEGER,
                    "IBB" INTEGER,
                    "WP" INTEGER,
                    "BK" INTEGER,
                    "GDP" INTEGER,
                    "GOAO" DOUBLE,
                    "SO9" DOUBLE,
                    "BB9" DOUBLE,
                    "KBB" DOUBLE,
                    "BABIP" DOUBLE,
                    "SB" INTEGER,
                    "CS" INTEGER,
                    "PK" INTEGER,
                    FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID),
                    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
                    FOREIGN KEY (TeamID) REFERENCES Team(TeamID)
                   );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TeamPitchingStats
                   (
                    TStatsID INTEGER PRIMARY KEY,
                    SeasonID INTEGER,
                    TeamID INTEGER,
                    "W" INTEGER,
                    "L" INTEGER,
                    "ERA" DOUBLE,
                    "G" INTEGER,
                    "GS" INTEGER,
                    "CG" INTEGER,
                    "SHO" INTEGER,
                    "SV" INTEGER,
                    "SVO" INTEGER,
                    "IP" DOUBLE,
                    "H" INTEGER,
                    "R" INTEGER,
                    "ER" INTEGER,
                    "HR" INTEGER,
                    "HB" INTEGER,
                    "BB" INTEGER,
                    "SO" INTEGER,
                    "WHIP" DOUBLE,
                    "AVG" DOUBLE,
                    "TBF" INTEGER,
                    "NP" INTEGER,
                    "PIP" DOUBLE,
                    "GF" INTEGER,
                    "HLD" INTEGER,
                    "IBB" INTEGER,
                    "WP" INTEGER,
                    "BK" INTEGER,
                    "GDP" INTEGER,
                    "GO" INTEGER,
                    "AO" INTEGER,
                    "GOAO" DOUBLE,
                    "SO9" DOUBLE,
                    "BB9" DOUBLE,
                    "KBB" DOUBLE,
                    FOREIGN KEY (SeasonID) REFERENCES Season(SeasonID),
                    FOREIGN KEY (TeamID) REFERENCES Team(TeamID)
                   );
    """)

    conn.commit()

def season_year(df:pd.DataFrame, conn:sqlite3.Connection, cursor:sqlite3.Cursor):
    year_set = set(df['Year'])
    for year in year_set:
        cursor.execute("INSERT OR IGNORE INTO Season (SeasonYear) VALUES (?);",(year, ))
    conn.commit()

def generate_sql_instructure(df:pd.DataFrame):
    dtype_map = {"int64":"INTEGER", 'float64':'DOUBLE', 'object':'DOUBLE', 'bool':'NOT', 'datatime64[ns]':'NOT'}
    SQL_instruct = str()
    for col, dtype in df.dtypes.items():
        sql_type = dtype_map.get(str(dtype), 'DOUBLE')
        SQL_instruct += f'"{col}" {sql_type},\n'
    print(SQL_instruct)

def insert_plyaer(df:pd.DataFrame, conn:sqlite3.Connection, cursor:sqlite3.Cursor):
    players = set(df['PLAYER'])
    print(players)
    for player in players:
        cursor.execute("INSERT OR IGNORE INTO Player (Name) VALUES (?);",(player, ))
    conn.commit()

def insert_team(df:pd.DataFrame, conn:sqlite3.Connection, cursor:sqlite3.Cursor):
    teams_list = set()
    for team, league in zip(df['TEAM'], df['LEAGUE']):
        teams_list.add(tuple([team, league]))
    
    for tl in teams_list:
        cursor.execute("INSERT OR IGNORE INTO Team (TeamName, League) VALUES (?,?);", (tl[0], tl[1]))

    conn.commit()

YEAR_RANGE = range(2003, 2024)

def normlize_col(col:str):
    return col.replace('/', '').strip()

def insert_playerpitching(df:pd.DataFrame, conn:sqlite3.Connection, cursor:sqlite3.Cursor, get_id_via_name, get_id_via_year, get_id_via_team):
    data_columns = [col for col in df.columns if col not in ["Year", "PLAYER", "TEAM"]]
    for _, row in tqdm(df.iterrows()):
        season_id = get_id_via_year[row['Year']]
        player_id = get_id_via_name[row['PLAYER']]
        team_id = get_id_via_team[abbr_to_name[row['TEAM']]]

        insert_data = row.drop(["Year", "PLAYER", "TEAM"])
        insert_data.index = [col.replace('/','') for col in insert_data.index]
        insert_data['SeasonID'] = season_id
        insert_data['PlayerID'] = player_id
        insert_data['TeamID'] = team_id

        columns = ', '.join(f'"{col}"' for col in insert_data.index)
        placeholders = ', '.join(['?'] * len(insert_data))
        values = tuple(insert_data.values)

        insert_sql = f"""
        INSERT INTO PitchingStats ({columns})
        VALUES ({placeholders});
        """

        cursor.execute(insert_sql, values)
        conn.commit()


def insert_teampitching(df:pd.DataFrame, conn:sqlite3.Connection, cursor:sqlite3.Cursor, get_id_via_name, get_id_via_year, get_id_via_team):
    for _, row in tqdm(df.iterrows()):
        season_id = get_id_via_year[row['Year']]
        team_id = get_id_via_team[row['TEAM']]

        insert_data = row.drop(["Year", "TEAM", "LEAGUE"])
        insert_data.index = [col.replace('/','') for col in insert_data.index]
        insert_data['SeasonID'] = season_id
        insert_data['TeamID'] = team_id

        columns = ', '.join(f'"{col}"' for col in insert_data.index)
        placeholders = ', '.join(['?'] * len(insert_data))
        values = tuple(insert_data.values)

        insert_sql = f"""
        INSERT INTO TeamPitchingStats ({columns})
        VALUES ({placeholders});
        """

        cursor.execute(insert_sql, values)
        conn.commit()

def get_id_from_dataframes(df_player:pd.DataFrame, df_team:pd.DataFrame, conn:sqlite3.Connection, cursor:sqlite3.Cursor):
    players = list(df_player['PLAYER'])
    teams = list(df_team['TEAM'])
    get_id_via_name = dict()
    get_id_via_year = dict()
    get_id_via_team = dict()
    for player in players:
        cursor.execute("SELECT PlayerID FROM Player WHERE Name = ?",(player,))
        name_result = cursor.fetchone()[0]
        if not name_result:
            continue
        get_id_via_name[player] = name_result
    
    for year in YEAR_RANGE:
        cursor.execute("SELECT SeasonID FROM Season WHERE SeasonYear = ?", (year,))
        year_result = cursor.fetchone()[0]
        if not year_result:
            continue
        get_id_via_year[year] = year_result

    for team in teams:
        cursor.execute("SELECT TeamID FROM Team WHERE TeamName = ?", (team,))
        team_result = cursor.fetchone()[0]
        
        if not team_result:
            continue
        get_id_via_team[team] = team_result

    return get_id_via_name, get_id_via_year, get_id_via_team

def get_abbr_to_name(path='./data/abbr_to_name.json'):
    with open(path) as f:
        data = json.load(f)
        return data


if __name__ == '__main__':
    
    conn, cursor = connect_to_db()
    
    df_player = pd.read_csv('data/player.csv')
    df_team = pd.read_csv('data/team.csv')

    abbr_to_name = get_abbr_to_name()

    #print(df_player)
    #print(df_team)

    #generate_sql_instructure(df_player)
    #generate_sql_instructure(df_team)

    create_tables(conn, cursor)

    season_year(df_team, conn, cursor)
    insert_plyaer(df_player, conn, cursor)
    insert_team(df_team, conn, cursor)

    get_id_via_name, get_id_via_year, get_id_via_team = get_id_from_dataframes(df_player, df_team, conn, cursor)
    insert_playerpitching(df_player, conn, cursor, get_id_via_name, get_id_via_year, get_id_via_team)
    insert_teampitching(df_team, conn, cursor, get_id_via_name, get_id_via_year, get_id_via_team)
    
    

    cursor.close()
from bs4 import BeautifulSoup
import requests
import time
from bs4 import BeautifulSoup
import openpyxl
from config.setting import *
from fetcher import fetch, fetch_team
from parser import pitching_parser, pitching_team_parser
from storage.save_csv import *

def player_part(session:requests.Session):
    results = fetch.get_all_data(session, PLAYER_URL, YEAR_RANGE)
    year_data = pitching_parser.parse_all_data(results)
    std_label = pitching_parser.get_std_label()
    exp_label = pitching_parser.get_exp_label()
    save_to_player_csv(std_label, exp_label, year_data)

def team_part(session:requests.Session):
    results = fetch_team.get_all_data(session, TEAM_URL, YEAR_RANGE)
    year_data = pitching_team_parser.parse_all_data(results)
    std_label = pitching_team_parser.get_std_label()
    exp_label = pitching_team_parser.get_exp_label()
    #save_to_team_xlsx(std_label, exp_label, year_data)
    save_to_team_csv(std_label, exp_label, year_data)
    pass

if __name__ == '__main__':
    session = requests.Session()
    
    player_part(session)
    team_part(session)

    exit()
"""
MLBScraper/
│
├── main.py                    # 程式進入點，負責執行整體流程
│
├── config/                    
│   └── settings.py            # 設定檔，放URL、headers、API key、儲存路徑等
│
├── fetcher/                   
│   └── fetch.py               # 網頁請求模組，負責向目標網站發送請求並獲取原始資料
│
├── parser/                    
│   └── pitching_parser.py     # 資料解析模組，解析HTML/JSON並提取所需欄位
│
├── storage/                   
│   └── save_csv.py            # 資料儲存模組，將處理過的資料存到CSV或資料庫中
│
├── utils/
│   └── helpers.py             # 公用工具，例如日誌、重試機制、進度條等
│
└── tests/
    └── test_parser.py         # 單元測試模組，測試parser正確性
"""
from bs4 import BeautifulSoup
import requests
from config.setting import *

def get_std_label():
    
    labels = []
    soup = BeautifulSoup(requests.get(f'{PLAYER_URL}2003?page=1&{STD_POST_FIX}').text, 'lxml')
    table_head = soup.select_one('thead tr').select('th')
    for th in table_head:
        labels.append(th.select_one('abbr').text)
    return labels

def get_exp_label():
    labels = []
    soup = BeautifulSoup(requests.get(f'{PLAYER_URL}2003?page=1&{EXP_POST_FIX}').text, 'lxml')
    table_head = soup.select_one('thead tr').select('th')
    for th in table_head:
        labels.append(th.select_one('abbr').text)
    return labels

def get_std_data(data:requests.Response):
    players_data = []
    soup = BeautifulSoup(data.text, 'lxml')
    players = soup.select('tbody > tr')
    
    for player in players:
        subsoup = BeautifulSoup(str(player), 'lxml')
        player_name_tag = subsoup.select('th>div>div>div>div>a>span')
        player_data = [tag.text for tag in subsoup.select('td')]
        player_name = player_name_tag[0].text+' '+player_name_tag[2].text
        players_data.append([player_name, player_data])
        #print('NAME:'+player_name.ljust(15)+'\t'+"DATA:"+str(player_data).rjust(100))

    return players_data

def get_exp_data(data:requests.Response):
    players_data = []
    soup = BeautifulSoup(data.text, 'lxml')
    players = soup.select('tbody > tr')
    
    for player in players:
        subsoup = BeautifulSoup(str(player), 'lxml')
        player_name_tag = subsoup.select('th>div>div>div>div>a>span')
        player_data = [tag.text for tag in subsoup.select('td')]
        player_name = player_name_tag[0].text+' '+player_name_tag[2].text
        players_data.append([player_name, player_data])
        #print('NAME:'+player_name.ljust(15)+'\t'+"DATA:"+str(player_data).rjust(100))

    return players_data

def parse_page_data(raw_pages_data):
    player_data = {}

    std_data = get_std_data(raw_pages_data[0])
    exp_data = get_exp_data(raw_pages_data[1])

    for data in std_data:
        player_data[data[0]] = {'Standard':data[1], 'Expanded':None}
    
    for data in exp_data:
        player_data[data[0]]['Expanded'] = data[1]

    # for key, value in player_data.items():
    #     print('NAME:'+str(key).ljust(15)+'\t'+"STD:"+str(value['Standard']).rjust(100))
    #     print('NAME:'+str(key).ljust(15)+'\t'+"EXP:"+str(value['Expanded']).rjust(100))

    return player_data

def parse_year_data(raw_years_data):
    year_player_data = {}#{NAME:{STD:DATA, EXP:DATA}}
    for page_data in raw_years_data:
        page_player_data = parse_page_data(page_data)
        year_player_data = year_player_data | page_player_data#union two dictionaries

    for key, value in year_player_data.items():
        print('NAME:'+str(key).ljust(15)+'\t'+"STD:"+str(value['Standard']).rjust(100))
        print('NAME:'+str(key).ljust(15)+'\t'+"EXP:"+str(value['Expanded']).rjust(100))

    return year_player_data
    

def parse_all_data(raw_totol_data):
    each_year_data = []
    for year_data in raw_totol_data:
        year_player_data = parse_year_data(year_data)
        each_year_data.append(year_player_data)

    return each_year_data

"""
raw_data_structure:
[outter p
    [year1
        [page1
            [std_data
            ],
            [exp_data
            ]
        ],
        [page2
        ],
        .
        .
        .
    ],
    [year2
        .
        .
        .
    ],
    .
    .
    .
]
"""
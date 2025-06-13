from bs4 import BeautifulSoup
import requests
from config.setting import *

def get_std_label():
    
    labels = []
    soup = BeautifulSoup(requests.get(f'{TEAM_URL}2003?page=1&{TEAM_STD_POST_FIX}').text, 'lxml')
    table_head = soup.select_one('thead tr').select('th')
    for th in table_head:
        labels.append(th.select_one('abbr').text)
    return labels

def get_exp_label():
    labels = []
    soup = BeautifulSoup(requests.get(f'{TEAM_URL}2003?page=1&{TEAM_EXP_POST_FIX}').text, 'lxml')
    table_head = soup.select_one('thead tr').select('th')
    for th in table_head:
        labels.append(th.select_one('abbr').text)
    return labels

def get_std_data(data:requests.Response):
    teams_data = []
    soup = BeautifulSoup(data.text, 'lxml')
    teams = soup.select('tbody > tr')
    
    for team in teams:
        subsoup = BeautifulSoup(str(team), 'lxml')
        team_name_tag = subsoup.select_one('th>div>div>div>div>a>span')
        team_data = [tag.text for tag in subsoup.select('td')]
        team_name = team_name_tag.text
        teams_data.append([team_name, team_data])
        #print('NAME:'+player_name.ljust(15)+'\t'+"DATA:"+str(player_data).rjust(100))

    return teams_data

def get_exp_data(data:requests.Response):
    teams_data = []
    soup = BeautifulSoup(data.text, 'lxml')
    teams = soup.select('tbody > tr')
    
    for team in teams:
        subsoup = BeautifulSoup(str(team), 'lxml')
        team_name_tag = subsoup.select_one('th>div>div>div>div>a>span')
        team_data = [tag.text for tag in subsoup.select('td')]
        team_name = team_name_tag.text
        teams_data.append([team_name, team_data])
        #print('NAME:'+player_name.ljust(15)+'\t'+"DATA:"+str(player_data).rjust(100))

    return teams_data

def parse_page_data(raw_pages_data):
    team_data = {}

    std_data = get_std_data(raw_pages_data[0])
    exp_data = get_exp_data(raw_pages_data[1])

    for data in std_data:
        team_data[data[0]] = {'Standard':data[1], 'Expanded':None}
    
    for data in exp_data:
        team_data[data[0]]['Expanded'] = data[1]

    # for key, value in player_data.items():
    #     print('NAME:'+str(key).ljust(15)+'\t'+"STD:"+str(value['Standard']).rjust(100))
    #     print('NAME:'+str(key).ljust(15)+'\t'+"EXP:"+str(value['Expanded']).rjust(100))

    return team_data

def parse_year_data(raw_years_data):

    year_player_data = parse_page_data(raw_years_data)#{NAME:{STD:DATA, EXP:DATA}}

    for key, value in year_player_data.items():
        print('NAME:'+str(key).ljust(30)+'\t'+"STD:"+str(value['Standard']).rjust(100))
        print('NAME:'+str(key).ljust(30)+'\t'+"EXP:"+str(value['Expanded']).rjust(100))

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
        std
        exp
    ],
    [year2
        std
        exp
    ],
    .
    .
    .

]
"""
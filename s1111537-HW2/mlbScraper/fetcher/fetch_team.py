import requests
from config.setting import *
from bs4 import BeautifulSoup

import time

def log(msg, end='\n'):
    if type(msg) != type(str):
        msg = str(msg)
    print(time.strftime('[%Y-%m-%d %H:%M:%S]'), msg, end = end)

def get_std_html(session:requests.Session, url:str)->requests.Response:
    
    response = session.get(f'{url}&{TEAM_STD_POST_FIX}')
    return response

def get_exp_html(session:requests.Session, url:str)->requests.Response:
    
    response = session.get(f'{url}&{TEAM_EXP_POST_FIX}')
    return response

def get_year_data(session, url, year):

    pass_url = url + str(year) + '?page={}'
    page = 1

    r_std = get_std_html(session, pass_url.format(page))
    r_exp = get_exp_html(session, pass_url.format(page))
    log(f"GET {pass_url}, page={page} Done, status_code={r_std.status_code},{r_exp.status_code}")


    return [r_std, r_exp]

def get_all_data(session, url, year_range:range):
    years_data = []

    for year in year_range:
        r = get_year_data(session, url, year)
        years_data.append(r)

    return years_data
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

COOKIE_BUTTON_SELECTOR = '#onetrust-accept-btn-handler'
EXPANDED_BUTTON_SELECTOR = '#stats-app-root > section > section > div.stats-navigation > div.stats-type-wrapper-KRUAKJx8 > div > div:nth-child(1) > div > div:nth-child(2)'

def log(msg, end='\n'):
    print(time.strftime('[%Y-%m-%d %H:%M:%S]')+msg, end=end)
#col_label = [lb.text for lb in soup.select('thead > tr > th > button > div > abbr')]

cookie = {"name":"_tt_enable_cookie", "value":"1"}

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://www.mlb.com/stats/2003")

log('request GET over')
try:
    accept_button = driver.find_element(By.CSS_SELECTOR, COOKIE_BUTTON_SELECTOR)
    accept_button.click()
except:
    pass


wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EXPANDED_BUTTON_SELECTOR)))
button = driver.find_element(By.CSS_SELECTOR, EXPANDED_BUTTON_SELECTOR)
button.click()

log("Click Over")
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#stats_index > main')))

#print(driver.title)
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

body = soup.select_one('#stats_index > main')

body_soup = BeautifulSoup(body.text, 'lxml')

print(body_soup.prettify())

col_label = [lb for lb in soup.select('thead > tr > th > button > div > abbr')]

for tag in col_label:
    print(tag)

#print(col_label)

driver.quit()
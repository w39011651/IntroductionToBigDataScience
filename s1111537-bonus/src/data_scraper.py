import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
import lxml
from typing import Dict, List, Any


year_selector = "#stats-app-root > section > section > div.stats-navigation > div.dropdowns-wrapper-IxKl1meY > div.bui-dropdown.stats-navigation.stats-dropdown-d3HK5t2w.display-mobile-HJi1LdrL.stats-filter-season.sm-DwCvPbGF.height-sm-J0GeOfXi.single-select.has-header > div > div > div.bui-dropdown__value-container.bui-dropdown__value-container--has-value.css-1hwfws3 > div"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_page(session:aiohttp.ClientSession, url:str):
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        raise e
    
def parse_player_data(html: str):
    parse = BeautifulSoup(html, 'lxml')
    year = parse.select_one(year_selector)
    print(year.text)

async def scrape_mlb_data(urls: Dict[str, str]):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for key, url in urls.items():
            tasks.append(fetch_page(session, url))
        
        pages = await asyncio.gather(*tasks, return_exceptions=True)

        for i, (key, page) in enumerate(zip(urls.keys(), pages)):
            parse_player_data(pages)


def run_scraper(urls: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    同步接口，運行非同步爬蟲。
    
    Args:
        urls: 爬取目標的 URL 字典
    
    Returns:
        爬取結果
    """
    return asyncio.run(scrape_mlb_data(urls))
    pass

if __name__ == '__main__':
    # 測試爬蟲
    test_urls = {
        'player': 'https://www.mlb.com/stats/pitching/2003',
        'team': 'https://www.mlb.com/stats/team/2003'
    }
    data = run_scraper(test_urls)
    # for table, records in data.items():
    #     print(f"{table}: {len(records)} records")
    
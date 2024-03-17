import requests
from bs4 import BeautifulSoup as BS
import datetime

SITE_URL = 'https://obhavo.uz/'


def get_weather(city):
    url = SITE_URL+city
    r = requests.get(url).content
    html = BS(r, "lxml")
    today = html.find('div', attrs={'class': 'current-day'}).text
    today_temp = html.find('div', attrs={'class': 'current-forecast'}).text.strip().replace('\n', ':').split(':')
    icon = html.find('div', attrs={'class': 'current-forecast'}).findChild('img')['src']
    weeks = html.find('table', attrs={'class': 'weather-table'}).findChildren('tr')
    first = True
    days = {}
    for week in weeks:
        if first:
            first = False
            continue
        days[week.find('td', attrs={'class': 'weather-row-day'}).findChild('div').text] = week.find('td', attrs={'class': 'weather-row-forecast'}).findChildren('span')

    return {'today': [today, today_temp, icon], 'week': days}

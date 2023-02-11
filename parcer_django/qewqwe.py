from typing import Optional

import requests
from bs4 import BeautifulSoup
import schedule
import time
import sqlite3
from requests import Response

CREATE_TABLE_HUB_DATA = """
    CREATE TABLE IF NOT EXISTS hab_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        URL TEXT,
        USER_NAME TEXT, 
        USER_LINK TEXT, 
        R_DATE TEXT
    )
"""


HOST = 'https://habr.com/'
URL = ['https://habr.com/ru/hub/programming/', 'https://habr.com/ru/hub/popular_science/']
HEADERS = {
    'accept': 'Accept: application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

connection = sqlite3.connect('hab_data2.db')
cursor = connection.cursor()

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS hab_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        URL TEXT,
        USER_NAME TEXT, 
        USER_LINK TEXT, 
        R_DATE TEXT
    )
""")


def get_html(url) -> Optional[Response]:
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response


def get_content(html: str) -> list[dict]:
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='tm-article-snippet')
    hab = []
    for item in items:
        if not item.find('a', class_='tm-user-info__username'):
            continue

        try:
            user_name = item.find('a', class_='tm-user-info__username').get_text(strip=True)
        except AttributeError:
            user_name = '--'

        try:
            user_url = item.find('a', class_='tm-user-info__username').get_text(strip=True)
        except AttributeError:
            user_url = HOST

        try:
            r_date = item.find('span', class_='tm-article-snippet__datetime-published').get_text(strip=True)
        except AttributeError:
            r_date = '--'

        hab.append(
            {
                'title': item.find('a', class_='tm-article-snippet__title-link').get_text(strip=True),
                'link': HOST + item.find('a', class_='tm-article-snippet__title-link').get('href'),
                'user_name': user_name,
                'user_url': user_url,
                'r_date': r_date
            }
        )
    return hab


def hab2(link: str, page):
    print(f'Парсим урл: {link}, страница {page}')

    html = get_html(link + f'page{page}')
    if not html:
        print('Не удалось получить стнаицу')
        return

    hab = get_content(html.text)

    cursor.executemany(
        "INSERT INTO hab_data (title, URL, USER_NAME, USER_LINK, R_DATE) "
        "VALUES (:title, :link, :user_name, :user_url, :r_date)",
        hab
    )

    connection.commit()


if __name__ == '__main__':

    for url in URL:
        for page in range(1, 50):
            hab2(url, page)


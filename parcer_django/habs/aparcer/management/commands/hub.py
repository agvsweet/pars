import requests
from bs4 import BeautifulSoup
import schedule
import time
import sqlite3
from django.core.management.base import BaseCommand
from aparcer.models import Product

class Command(BaseCommand):
    help = 'парсинг habr-а'
    def handle(self, *args, **options):
        p = Product()
        p.parse_all()

connection = sqlite3.connect('hab_data2.db')
cursor = connection.cursor()
cursor.executescript("CREATE TABLE IF NOT EXISTS hab_data (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, URL TEXT, USER_NAME TEXT, USER_LINK TEXT, R_DATE TEXT)")

def job(html):
    print(get_content(html.text))


HOST = 'https://habr.com/'
URL = ['https://habr.com/ru/hub/programming/', 'https://habr.com/ru/hub/popular_science/']
HEADERS = {
    'accept': 'Accept: application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='tm-article-snippet')
    hab = []
    for item in items:
        hab.append(
            {
                'title': item.find('a', class_='tm-article-snippet__title-link').get_text(strip=True),
                'link': HOST + item.find('a', class_='tm-article-snippet__title-link').get('href'),
                'user_name': item.find('a', class_='tm-user-info__username').get_text(strip=True),
                'user_url': HOST + item.find('a', class_='tm-user-info__userpic').get('href'),
                'r_date': item.find('span', class_='tm-article-snippet__datetime-published').get_text(strip=True)
            }
        )
    return hab

def hab2(link):
    html = get_html(link)
    hab = get_content(html.text)
    cursor.executemany(
        "INSERT INTO hab_data (title, URL, USER_NAME, USER_LINK, R_DATE) VALUES (:title, :link, :user_name, :user_url, :r_date)",
        hab)
    connection.commit()
    schedule.every(600).seconds.do(lambda: job(html))

for url in URL:
    hab2(url)
connection.close()

while True:
    schedule.run_pending()

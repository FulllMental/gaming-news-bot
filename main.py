import pathlib
import time
from datetime import datetime
from os.path import splitext
from urllib.parse import unquote, urlsplit

import requests
from bs4 import BeautifulSoup as BS
from environs import Env

from shazoo_parse import get_all_links
from telegram_bot import bot_message


def get_article_text(article_link):
    response = requests.get(article_link)
    response.raise_for_status()

    article = BS(response.content, 'html.parser')
    results = article.find_all('p')
    article = ''
    for i in results:
        article += f'{i.text}\n'
    return article


def download_shazoo_picture(directory, shazoo_picture_url):
    extension = get_picture_extension(shazoo_picture_url)
    pathlib.Path(f'{directory}').mkdir(parents=True, exist_ok=True)
    filename = f'{directory}/hubble.{extension}'

    response = requests.get(shazoo_picture_url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_picture_extension(shazoo_picture_url):
    link_split = urlsplit(shazoo_picture_url)
    file_name = unquote(link_split[2])
    file_extension = splitext(file_name)
    return file_extension[1]


if __name__ == '__main__':
    env = Env()
    env.read_env()
    pause_time = env.int('PAUSE_TIME')
    last_check_date = env('LAST_CHECK_DATE')
    shazoo_url = env('SHAZOO_URL')
    blacklist = env.list('BLACKLIST')
    directory = 'shazoo_images'

    while True:
        shazoo_news = get_all_links(shazoo_url, last_check_date, blacklist)
        for post in shazoo_news:
            bot_message(article_link=post['article_link'], article_title=post['article_title'])
            # shazoo_picture_url = post['picture_link']
            # download_shazoo_picture(directory, shazoo_picture_url)

        last_check_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
        print(f'Пост отправлен, следующий пост будет только тот, что запостили после {last_check_date}')
        time.sleep(pause_time)


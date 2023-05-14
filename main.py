import logging
import pathlib
import time
from datetime import datetime
from os.path import splitext
from urllib.parse import unquote, urlsplit

import requests
from bs4 import BeautifulSoup as BS
from environs import Env

from shazoo_parse import get_all_posts, get_actual_links
from telegram_bot import bot_message


def get_article_text(article_link):
    article_response = requests.get(article_link)
    article_response.raise_for_status()

    article = BS(article_response.content, 'lxml')
    article_indents = article.find_all('p')
    article = ''
    for indent in article_indents:
        article += f'{indent.text}\n'
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
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    env = Env()
    env.read_env()

    pause_time = env.int('PAUSE_TIME')
    shazoo_url = env('SHAZOO_URL')
    blacklist = env.list('BLACKLIST')

    # directory = 'shazoo_images'

    logging.warning('Бот запущен...')
    last_check_date = 0

    last_check_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    # last_check_date = '2023-05-14T06:00:00'
    while True:
        posts = get_all_posts(shazoo_url)
        shazoo_news = get_actual_links(posts, blacklist, last_check_date)
        last_check_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")

        logging.warning(f'Следующий пост будет после {last_check_date}UTC')

        for post in shazoo_news:
            bot_message(article_link=post['article_link'], article_title=post['article_title'])

            # shazoo_picture_url = post['picture_link']
            # download_shazoo_picture(directory, shazoo_picture_url)

            logging.warning('Пост отправлен...')
            time.sleep(pause_time)

        if shazoo_news:
            shazoo_news.clear()
            continue

        logging.warning(f'Ожидание новой итерации через {pause_time}...')
        time.sleep(pause_time)


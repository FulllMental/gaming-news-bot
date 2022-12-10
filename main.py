import datetime
import time

from environs import Env

from shazoo_parse import get_all_links, download_shazoo_picture
from telegram_bot import bot_message

if __name__ == '__main__':
    env = Env()
    env.read_env()
    pause_time = env('PAUSE_TIME')
    last_check_date = env('LAST_CHECK_DATE')
    shazoo_url = env('SHAZOO_URL')
    directory = 'shazoo_images'

    while True:
        shazoo_news = get_all_links(shazoo_url, last_check_date)
        for post in shazoo_news:
            shazoo_picture_url = post['picture_link']
            bot_message(article_link=post['article_link'], article_title=post['article_title'])
            download_shazoo_picture(directory, shazoo_picture_url)

        last_check_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
        print(f'Пост отправлен, следующий пост будет только тот, что запостили после {last_check_date}')
        time.sleep(int(pause_time))


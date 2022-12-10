import pathlib
from os.path import splitext
from urllib.parse import unquote, urlsplit

import requests
from bs4 import BeautifulSoup as BS


def get_all_links(shazoo_url, last_check_date):
    response = requests.get(shazoo_url)
    response.raise_for_status()

    news = []
    html = BS(response.content, 'html.parser')
    posts = html.find_all('div', class_="flex flex-col gap-2 py-6 first:pt-0")
    for post in posts:
        post_date = post.time.attrs['datetime'][:-11]
        if last_check_date >= post_date:
            return news
        ppt = post.find('div', class_='flex-shrink-0')
        article_title = ppt.a['title']
        article_link = ppt.a['href']

        news.append({'article_title': article_title,
                     'picture_link': ppt.img['src'],
                     'article_link': article_link})
                     # 'article_text': get_article_text(article_link)})
    return news


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
    extension = get_extension(shazoo_picture_url)
    pathlib.Path(f'{directory}').mkdir(parents=True, exist_ok=True)
    filename = f'{directory}/hubble.{extension}'

    response = requests.get(shazoo_picture_url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def get_extension(shazoo_picture_url):
    link_split = urlsplit(shazoo_picture_url)
    file_name = unquote(link_split[2])
    file_extension = splitext(file_name)
    return file_extension[1]


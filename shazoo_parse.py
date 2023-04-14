import requests
from bs4 import BeautifulSoup as BS

from environs import Env



def get_all_links(shazoo_url, last_check_date, blacklist):
    site_response = requests.get(shazoo_url)
    site_response.raise_for_status()

    shazoo_news = []
    shazoo_soup = BS(site_response.content, 'lxml')
    posts_selector = 'div.py-6.gap-2'
    posts = shazoo_soup.select(posts_selector)

    for post in posts:
        post_date = post.time.attrs['datetime'][:-11]

        if last_check_date >= post_date:
            return shazoo_news

        post_summary = post.find('div', class_='flex-shrink-0')
        article_title = post_summary.a['title']

        if check_blacklist(article_title, blacklist):
            continue

        shazoo_news.append(
            {
                'article_title': article_title,
                'picture_link': post_summary.img['src'],
                'article_link': post_summary.a['href']
            }
        )
    return shazoo_news


def check_blacklist(article_title, blacklist):
    for banword in blacklist:
        if banword in article_title.lower():
            return True
    return False


if __name__ == '__main__':
    env = Env()
    env.read_env()

    last_check_date = env('LAST_CHECK_DATE')
    shazoo_url = env('SHAZOO_URL')
    blacklist = env.list('BLACKLIST')

    get_all_links(shazoo_url, last_check_date, blacklist)
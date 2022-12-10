import requests
from bs4 import BeautifulSoup as BS


def get_all_links(shazoo_url, last_check_date, blacklist):
    response = requests.get(shazoo_url)
    response.raise_for_status()

    shazoo_news = []
    html = BS(response.content, 'html.parser')
    posts = html.find_all('div', class_="flex flex-col gap-2 py-6 first:pt-0")
    for post in posts:
        post_date = post.time.attrs['datetime'][:-11]
        if last_check_date >= post_date:
            return shazoo_news
        ppt = post.find('div', class_='flex-shrink-0')
        article_title = ppt.a['title']
        if check_blacklist(article_title, blacklist):
            continue
        shazoo_news.append(
            {
                'article_title': article_title,
                'picture_link': ppt.img['src'],
                'article_link': ppt.a['href']
            }
        )
    return shazoo_news


def check_blacklist(article_title, blacklist):
    for banword in blacklist:
        if banword in article_title.lower():
            return True
    return False

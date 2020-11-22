import requests
from bs4 import BeautifulSoup


def get_news(url):
    page = requests.get(url)
    news_list = []

    soup = BeautifulSoup(page.content, 'html.parser')

    news_div = soup.find_all(class_='search-result-contend-block')

    for news in news_div:
        news_link = news.find('a')['href']
        news_heading = news.find('h2').text
        news_text_ = news.find('p', class_='text-left').text
        news_text = news_text_.replace('Colombo (News 1st);', '')
        news_date = news.find(class_='news-set-date').find('p').text

        news_dict = {
            'news_link': news_link,
            'news_heading': news_heading,
            'news_text': news_text,
            'news_date': news_date,
        }

        news_list.append(news_dict)

    return news_list

    # print(news_list)

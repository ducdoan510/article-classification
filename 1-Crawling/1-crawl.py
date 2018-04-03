import string

import os

import requests
import time
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
import re
import pandas as pd

from decouple import config

API_KEY = config('API_KEY')


##### PART I: Crawling data using API and BeautifulSoup ######

newsapi = NewsApiClient(api_key=API_KEY)

source_ids = ['ars-technica', 'techcrunch', 'techradar', 'the-verge', 'wired', 'cnn', 'crypto-coins-news',
              'bbc-news', 'the-economist', 'reuters', 'recode', 'new-scientist', 'business-insider']
# source_ids = ['fox-news']
page_size = 100

number_of_articles = newsapi.get_everything(q='technology',
                                 sources=','.join(source_ids),
                                 from_parameter='2018-01-01',
                                 to='2018-04-11',
                                 language='en',
                                 sort_by='relevancy',
                                 page=1,
                                 page_size=100)['totalResults']

page = 1
number_of_articles -= (page - 1) * 100
while number_of_articles > 0:
    print("Fetching page %d, page size %d" % (page, page_size))

    articles = newsapi.get_everything(q='technology',
                                     sources=','.join(source_ids),
                                     from_parameter='2018-01-01',
                                     to='2018-04-11',
                                     language='en',
                                     sort_by='relevancy',
                                     page=page,
                                     page_size=page_size)['articles']

    for article in articles:
        print(article['title'], article['url'])
        article['source'] = article['source']['id']
        if article['url'].endswith(".mp4") or article['url'].endswith(".mp3"):
            continue
        try:
            article_body = requests.get(article['url']).content
            article['raw_html'] = article_body
        except Exception as e:
            print("...Error fetching html")
            continue

        time.sleep(0.05)

    print("Finish preprocessing...")

    df = pd.DataFrame(articles)
    df.to_csv(os.path.join("csv", "page_%d.csv" % (page + 99)), index=False)

    page += 1
    number_of_articles -= page_size



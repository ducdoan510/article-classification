import datetime
import os

import requests
import time
from newsapi import NewsApiClient
import pandas as pd

from decouple import config

API_KEY = config('API_KEY')

##### PART I: Crawling data using API and BeautifulSoup ######

newsapi = NewsApiClient(api_key=API_KEY)

source_ids = {
    "sport": ["bbc-sport", "espn", "four-four-two", "fox-sports", "the-sport-bible"],
    "politics": ["reuters", "cnn", "bbc-news", "politico", "abc-news"],
    "technology": ["ars-technica", "techcrunch", "techradar", "new-scientist"],
    "entertainment": ["buzzfeed", "entertainment-weekly", "mtv-news", "mtv-news-uk"],
    "business": ["the-wall-street-journal", "business-insider", "the-economist", "bloomberg"]
}

page_size = 100

is_first_time = True
if os.path.exists(os.path.join(config('DATA_FOLDER'), "csv", "data.csv")):
    print("Crawling new data...")
    is_first_time = False
else:
    print("Crawling for the first time...")

for key in source_ids.keys():
    if is_first_time:
        number_of_articles = newsapi.get_everything(q=key, sources=','.join(source_ids[key]), language='en', sort_by='relevancy', page=1, page_size=100)['totalResults']
    else:
        number_of_articles = newsapi.get_everything(q=key, sources=','.join(source_ids[key]), language='en', sort_by='relevancy', page=1, page_size=100, from_parameter=datetime.date.today().strftime("%Y-%m-%d"))['totalResults']

    print("****Crawling articles of topic: %s" % key.upper())

    page = 1
    number_of_articles = min(number_of_articles, 3000) - (page - 1) * 100
    while number_of_articles > 0:
        print("Fetching page %d, page size %d" % (page, page_size))

        if is_first_time:
            articles = newsapi.get_everything(q=key,
                                             sources=','.join(source_ids[key]),
                                             language='en',
                                             sort_by='relevancy',
                                             page=page,
                                             page_size=page_size)['articles']
        else:
            articles = newsapi.get_everything(q=key,
                                              sources=','.join(source_ids[key]),
                                              language='en',
                                              sort_by='relevancy',
                                              page=page,
                                              page_size=page_size,
                                              from_parameter=datetime.date.today().strftime("%Y-%m-%d"))['articles']

        for article in articles:
            print(article['title'], article['url'])
            article['source'] = article['source']['id']
            if article['url'].endswith(".mp4") or article['url'].endswith(".mp3") or "video" in article['url']:
                continue
            try:
                r = requests.get(article['url'])
                if r.status_code == 200:
                    article['raw_html'] = r.content
                else:
                    print(r.status_code, end = " invalid status code ")
                    article['raw_html'] = article['description']
            except:
                print("Error fetching url...")
                continue

            time.sleep(0.05)

        print("Finish preprocessing...Found %d articles" % len(articles))

        df = pd.DataFrame(articles)
        df.to_csv(os.path.join("csv", "%s_%d.csv" % (key, page)), index=False)

        page += 1
        number_of_articles -= page_size


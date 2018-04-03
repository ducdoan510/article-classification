import os
import re
import string

import pandas as pd
from bs4 import BeautifulSoup


def get_main_content_identifier(source_name):
    if source_name == "ars-technica":
        return {"value": "article-content", "by": "class"}
    if source_name == "techcrunch":
        return {"value": "article-content", "by": "class"}
    if source_name == "techradar":
        return {"value": "article-body", "by": "id"}
    if source_name == "the-verge":
        return {"value": "l-article-body-segment", "by": "class"}
    if source_name == "wired":
        return {"value": "article-main-component", "by": "class"}
    if source_name == "cnn":
        return {"value": "pg-rail-tall__body", "by": "class"}
    if source_name == "crypto-coins-news":
        return {"value": "entry-content", "by": "class"}
    if source_name == "bbc-news":
        return {"value": "content-main", "by": "class"}
    if source_name == "the-economist":
        return {"value": "blog-post__text", "by": "class"}
    if source_name == "reuters":
        return {"value": "body_1gnLA", "by": "class"}
    if source_name == "recode":
        return {"value": "c-entry-content", "by": "class"}
    if source_name == "new-scientist":
        return {"value": "article-content", "by": "class"}
    if source_name == "business-insider":
        return {"value": "the_bi_content", "by": "id"}
    if source_name == 'fox-news':
        return {"value": "article-body", "by": "class"}


def convert_html_to_text(row):
    html = row['raw_html']
    source_name = row['source']
    default = row['description']

    try:
        bs_obj = BeautifulSoup(html, 'lxml')
    except:
        bs_obj = BeautifulSoup(default, 'lxml')

    scripts = bs_obj.select("script")
    for script in scripts:
        script.decompose()

    styles = bs_obj.select("style")
    for style in styles:
        style.decompose()

    identifier = get_main_content_identifier(source_name)
    try:
        if identifier["by"] == "class":
            element = bs_obj.select("." + identifier["value"])[0]
        else:
            element = bs_obj.select("#" + identifier["value"])[0]
    except IndexError:
        element = bs_obj

    text = element.getText(separator=" ").replace("b\'", "").replace("\\n", '\n').replace("\\t", "\t").replace("\\r", "\r").replace("\\", " ").strip()
    text = re.sub(r'\b[a-z\d]*\d+[a-z\d]*\b', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text)

    if bool(re.match('\s*forbidden', text, re.I)):
        text = default

    regex = re.compile('[%s]' % re.escape(string.punctuation))
    text = regex.sub(' ', text)
    text = re.sub(r'\s+', ' ', text)
    # print("----")
    # print(text)
    return text


##### PART II: Combine data into single csv file #####

data_folder = os.path.join("..", "data")
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

dfs = []
for page in range(1, 103):
    df = pd.read_csv(os.path.join("csv", "page_%d.csv" % page))
    df['text'] = df.apply(convert_html_to_text, axis=1)

    df = df[['description', 'publishedAt', 'source', 'title', 'url', 'urlToImage', 'text']]
    dfs.append(df)
    # break

pd.concat(dfs).to_csv(os.path.join(data_folder, "data.csv"), index=False, encoding='utf-8')
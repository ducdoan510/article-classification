import glob
import os
import re
import string

import pandas as pd
import sys
from bs4 import BeautifulSoup
from decouple import config
from sklearn.externals import joblib

data_folder = config("DATA_FOLDER")
categories = ["business", "entertainment", "politics", "sport", "technology"]
is_first_time = not os.path.exists(os.path.join(data_folder, "csv", "data.csv"))
if not is_first_time:
    vectorizer = joblib.load(os.path.join(data_folder, 'pkl', 'vectorizer.pkl'))
    transformer = joblib.load(os.path.join(data_folder, 'pkl', 'transformer.pkl'))
    classifier = joblib.load(os.path.join(data_folder, 'pkl', 'classifier.pkl'))

def get_main_content_identifier(source_name):
    if source_name == "ars-technica":
        return {"value": "article-content", "by": "class"}
    if source_name == "techcrunch":
        return {"value": "article-content", "by": "class"}
    if source_name == "techradar":
        return {"value": "article-body", "by": "id"}
    if source_name == "new-scientist":
        return {"value": "article-content", "by": "class"}

    if source_name == "cnn":
        return {"value": "pg-rail-tall__body", "by": "class"}
    if source_name == "bbc-news":
        return {"value": "content-main", "by": "class"}
    if source_name == "reuters":
        return {"value": "body_1gnLA", "by": "class"}
    if source_name == 'politico':
        return {"value": "story-main-content", "by": "class"}
    if source_name == 'abc-news':
        return {"value": "article-body", "by": "class"}

    if source_name == 'bbc-sport':
        return {"value": "story-body", "by": "id"}
    if source_name == 'fox-sports':
        return {"value": "entry-content", "by": "class"}
    if source_name == 'espn':
        return {"value": "article", "by": "class"}
    if source_name == 'four-four-two':
        return {"value": "node-content", "by": "class"}

    if source_name == "business-insider":
        return {"value": "the_bi_content", "by": "id"}
    if source_name == "the-economist":
        return {"value": "blog-post__text", "by": "class"}
    if source_name == "the-wall-street-journal":
        return {"value": "article_sector", "by": "id"}
    if source_name == "bloomberg":
        return {"value": "content-well", "by": "class"}
    return {"value": "article-body", "by": "class"}


def format_text(text, default):
    text = re.sub(r'\b[a-z\d]*\d+[a-z\d]*\b', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text)

    if bool(re.match('\s*forbidden', text, re.I)):
        text = default

    regex = re.compile('[%s]' % re.escape(string.punctuation))
    text = regex.sub(' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def convert_html_to_text(row):
    html = row['raw_html']
    source_name = row['source']
    default = row['description']

    try:
        bs_obj = BeautifulSoup(html, 'lxml')
    except:
        # print(default)
        # print(html)
        return format_text(default, "")

    scripts = bs_obj.select("script")
    for script in scripts:
        script.decompose()

    styles = bs_obj.select("style")
    for style in styles:
        style.decompose()

    codeblocks = bs_obj.select("pre > code")
    for codeblock in codeblocks:
        codeblock.decompose()

    identifier = get_main_content_identifier(source_name)
    try:
        if identifier["by"] == "class":
            element = bs_obj.select("." + identifier["value"])[0]
        else:
            element = bs_obj.select("#" + identifier["value"])[0]
    except IndexError:
        element = bs_obj

    text = element.getText(separator=" ").replace("b\'", "").replace("\\n", '\n').replace("\\t", "\t").replace("\\r", "\r").replace("\\", " ").strip()
    text = format_text(text, default)
    # print("----")
    # print(text)
    return text.lower()


def convert_category_to_string(row):
    return categories[row['category'] - 1]

dest_data_folder = os.path.join(data_folder, "csv")
source_data_folder = "csv"

csv_files = glob.glob(os.path.join(source_data_folder, "*.csv"))

# read data from each csv file in csv folder
dfs = []
for csv_file in csv_files:
    print("Reading file " + csv_file)
    df = pd.read_csv(csv_file).dropna(axis=0, subset=['description', 'raw_html'], how='any')
    df['text'] = df.apply(convert_html_to_text, axis=1)
    df['category'] = csv_file.split(os.sep)[-1].split("_")[0]

    df = df[['description', 'publishedAt', 'source', 'title', 'url', 'urlToImage', 'text', 'category']]
    dfs.append(df)

if len(dfs) == 0:
    sys.exit("No more new articles...")

combined_data = pd.concat(dfs, ignore_index=True)

# if not the first time, use existing model to predict category
if not is_first_time:
    corpus = []
    for index, row in combined_data.iterrows():
        corpus.append(row['text'])

    X_counts = vectorizer.transform(corpus)
    X = transformer.transform(X_counts)
    combined_data['category'] = classifier.predict(X)
    combined_data['category'] = combined_data.apply(convert_category_to_string, axis=1)

# merge with existing data
if is_first_time:
    finalized_data = combined_data
else:
    existing = pd.read_csv(os.path.join(dest_data_folder, "data.csv"))
    finalized_data = pd.concat([existing, combined_data], ignore_index=True)

finalized_data['id'] = finalized_data.index
finalized_data.to_csv(os.path.join(dest_data_folder, "data.csv"), index=False, encoding='utf-8')

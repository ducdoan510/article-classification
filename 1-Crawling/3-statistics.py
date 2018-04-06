import os
import sys
import pandas as pd

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

processed_data_path = os.path.join("..", "data", "csv", "data.csv")
df = pd.read_csv(processed_data_path).dropna(axis=0, subset=['text'])
df.to_csv(processed_data_path, index=False, encoding='utf-8')

f = open("summary.txt", "w")
stdout = sys.stdout
sys.stdout = f

corpus = set([])
total_words = 0
for index, row in df.iterrows():
    words = row['text'].split()
    for word in words:
        corpus.add(word.lower())
    total_words += len(words)
    row['category'] = row['category'].split("_")[0]


print("Statistics for collected data")
print("-----------------------------")

print("Number of records: ", df.shape[0])
print("Number of words: ", total_words)
print("Number of unique words: ", len(corpus))

sys.stdout = stdout
f.close()


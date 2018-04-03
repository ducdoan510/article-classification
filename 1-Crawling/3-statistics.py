import os
import sys
import pandas as pd

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

processed_data_path = os.path.join("..", "data", "data.csv")
df = pd.read_csv(processed_data_path)

f = open("summary.txt", "w")
stdout = sys.stdout
sys.stdout = f

corpus = []
for index, row in df.iterrows():
    corpus.append(row['text'])

# min_df=10, stop_words=stopwords.words('english')
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
count_result = X.toarray()

print("Statistics for collected data")
print("-----------------------------")

print("Number of records: ", count_result.shape[0])
print("Number of words: ", count_result.sum())
print("Number of unique words: ", count_result.shape[1])

sys.stdout = stdout
f.close()

# count_result_sum = count_result.sum(axis=0)
# feature_names = vectorizer.get_feature_names()
# lis = []
# for feature in feature_names:
#     index = vectorizer.vocabulary_.get(feature)
#     lis.append([count_result_sum[index], feature])
#
# lis = sorted(lis)
# for i in range(len(lis)):
#     print(i, lis[i][1], lis[i][0])

# print(vectorizer.stop_words_)

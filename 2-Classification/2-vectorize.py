import os

import pickle

import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


filename = input("Enter the csv file name without .csv: ")
data_folder = os.path.join("..", "data")

corpus = []
df = pandas.read_csv(os.path.join(data_folder, "csv", filename + ".csv"))


for index, row in df.iterrows():
    corpus.append(row['text'])

print("Corpus length: ", len(corpus))

vectorizer = CountVectorizer(min_df=10)
X = vectorizer.fit_transform(corpus)

transformer = TfidfTransformer(smooth_idf=False)
X_tfidf = transformer.fit_transform(X)
print(X_tfidf.shape)
# print(X_tfidf.toarray())


with open(os.path.join(data_folder, "pkl", filename + ".pkl"), 'wb') as f:
    pickle.dump(X_tfidf, f)



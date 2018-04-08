import os

import numpy as np
import pandas as pd
import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


def convert_category(row):
    category = row['category']
    if category == 'business':
        return 1
    if category == "entertainment":
        return 2
    if category == "politics":
        return 3
    if category == "sport":
        return 4
    return 5

option = input("Select the preprocess option you chose:\n1 - lowercase + stopwords\n2 - lowercase + stopwords + stemming\n3 - lowercase\n")

if option == "1":
    filename = "data_processed"
elif option == "3":
    filename = "data_lowercase"
else:
    filename = "data_processed_stemmed"

data_folder = os.path.join("..", "data")


# read train data
df_train = pd.read_csv(os.path.join(data_folder, "csv", filename + "_train.csv"))
df_train['category_number'] = df_train.apply(convert_category, axis=1)
target_train = df_train['category_number'].values

train_corpus = []
for index, row in df_train.iterrows():
    train_corpus.append(str(row['text']))

vectorizer = CountVectorizer(min_df=10)
X_train_count = vectorizer.fit_transform(train_corpus)
transformer = TfidfTransformer(smooth_idf=False)
X_train = transformer.fit_transform(X_train_count)
print(X_train.shape)


# read test data
df_test = pd.read_csv(os.path.join(data_folder, "csv", filename + "_test.csv"))
df_test['category_number'] = df_test.apply(convert_category, axis=1)
target_test = df_test['category_number'].values

test_corpus = []
for index, row in df_test.iterrows():
    test_corpus.append(str(row['text']))

X_test_counts = vectorizer.transform(test_corpus)
X_test = transformer.transform(X_test_counts)


# train data and predict
start_time = time.time()

classifier = MultinomialNB().fit(X_train, target_train)
predicted = classifier.predict(X_test)
print(np.mean(predicted == target_test))

print(time.time() - start_time)

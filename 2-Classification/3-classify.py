import os

import numpy as np
import pandas as pd
import time
import sys
from decouple import config
from sklearn import metrics
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

categories = ["business", "entertainment", "politics", "sport", "technology"]


def convert_category_to_number(row):
    category = row['category']
    if category == 'business': return 1
    if category == "entertainment": return 2
    if category == "politics": return 3
    if category == "sport": return 4
    return 5


if len(sys.argv) >= 3: filename = sys.argv[2]
else: filename = "data_processed"


data_folder = config("DATA_FOLDER")

# read train data
df_train = pd.read_csv(os.path.join(data_folder, "csv", filename + "_train.csv"))
df_train['category_number'] = df_train.apply(convert_category_to_number, axis=1)
target_train = df_train['category_number'].values

train_corpus = []
for index, row in df_train.iterrows():
    train_corpus.append(str(row['text']))

vectorizer = CountVectorizer(min_df=10)
X_train_count = vectorizer.fit_transform(train_corpus)
transformer = TfidfTransformer(smooth_idf=False)
X_train = transformer.fit_transform(X_train_count)

joblib.dump(vectorizer, os.path.join(data_folder, 'pkl', 'vectorizer.pkl'))
joblib.dump(transformer, os.path.join(data_folder, 'pkl', 'transformer.pkl'))

# read test data
df_test = pd.read_csv(os.path.join(data_folder, "csv", filename + "_test.csv"))
df_test['category_number'] = df_test.apply(convert_category_to_number, axis=1)
target_test = df_test['category_number'].values

test_corpus = []
for index, row in df_test.iterrows():
    test_corpus.append(str(row['text']))

X_test_counts = vectorizer.transform(test_corpus)
X_test = transformer.transform(X_test_counts)

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)
print()

# train data and predict
start_time = time.time()

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    DecisionTreeClassifier(max_depth=5),
]

classifiers_name = ['K Nearest Neighbors', 'Support Vector Machine', 'Decision Tree']

classifiers.append(VotingClassifier(estimators=[(classifiers_name[i], classifiers[i]) for i in range(len(classifiers))], voting='hard'))
classifiers_name.append('Ensemble Learning')

for i in range(0, len(classifiers)):
    classifier = classifiers[i]
    print("***Start training data with classifier:", classifiers_name[i])

    start_time = time.time()
    classifier_fit = classifier.fit(X_train, target_train)
    print("Training time for %d records: %.4f" % (X_train.shape[0], time.time() - start_time))

    start_time = time.time()
    predicted = classifier_fit.predict(X_test)
    np.save(os.path.join(data_folder, "npy", "predicted_%s.npy" % (classifiers_name[i])), predicted)

    print("Testing time for %d records: %.4f" % (X_test.shape[0], time.time() - start_time))
    print("Average accuracy:", np.mean(predicted == target_test))
    print("Classification report: ")
    print(metrics.classification_report(target_test, predicted, digits=4, target_names=categories))

    confusion_matrix = metrics.confusion_matrix(target_test, predicted)
    np.save(os.path.join(data_folder, "npy", "%s_%s.npy" % (filename, classifiers_name[i])), confusion_matrix)

    if i == len(classifiers) - 1:
        joblib.dump(classifiers[i], os.path.join(data_folder, 'pkl', 'classifier.pkl'))


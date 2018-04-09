import pandas as pd
import os
import nltk
from decouple import config

stop_words = nltk.corpus.stopwords.words()


def format_text(row, is_processed):
    text = row['text']
    text = text.lower()

    if is_processed:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])

    return text


data_path = os.path.join(config("DATA_FOLDER"), "csv")

print("Lowercase all text...")
df = pd.read_csv(os.path.join(data_path, "data.csv"))
df['text'] = df.apply(format_text, args=(False,), axis=1)
df.to_csv(os.path.join(data_path, "data_lowercase.csv"), index=False)
print("Your lowercase data can be found in: " + os.path.abspath(os.path.join(data_path, "data_lowercase.csv")))


print("Processing data...")
df = pd.read_csv(os.path.join(data_path, "data.csv"))
df['text'] = df.apply(format_text, args=(True,), axis=1)
df.to_csv(os.path.join(data_path, "data_processed.csv"), index=False)
print("Your processed data can be found in: " + os.path.abspath(os.path.join(data_path, "data_processed.csv")))

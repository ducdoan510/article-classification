import pandas as pd
import os
import nltk

stop_words = set(nltk.corpus.stopwords.words('english'))
stemming = False
lemmatizing = False


def format_text(row):
    text = row['text']
    text = text.lower()

    if stemming:
        stemmer = nltk.stem.PorterStemmer()
        text = " ".join([stemmer.stem(word) for word in text.split() if word not in stop_words])
    elif lemmatizing:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    else:
        text = " ".join([word for word in text.split() if word not in stop_words])

    return text


option = input("Select one of the preprocess option below:\n1-stopwords\n2-stopwords + stemming\n3-stopwords + lemmatizing\n")
if option.strip() == "2":
    stemming = True
    output_filename = "data_processed_stemmed.csv"
elif option.strip() == "3":
    lemmatizing = True
    output_filename = "data_processed_lemmatized.csv"
else:
    output_filename = "data_processed.csv"


data_path = os.path.join("..", "data", "csv")
df = pd.read_csv(os.path.join(data_path, "data.csv"))

df['text'] = df.apply(format_text, axis=1)

df.to_csv(os.path.join(data_path, output_filename), index=False)

print("Finish preprocessing...")
print("Your processed data can be found in: " + os.path.abspath(os.path.join(data_path, output_filename)))

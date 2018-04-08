import pandas as pd
import os
import nltk

stop_words = set(nltk.corpus.stopwords.words('english'))
lemmatizing = False
remove_stop_words = False


def format_text(row):
    text = row['text']
    text = text.lower()

    if lemmatizing:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    elif remove_stop_words:
        text = " ".join([word for word in text.split() if word not in stop_words])

    return text


option = input("Select one of the option below (Enter 1 or 2):\n 1 - lowercase original text\n 2 (default) - lowercase original text, remove stop words, lemmatize text\n")
if option == "1":
    output_filename = "data_lowercase.csv"
else:
    lemmatizing = True
    remove_stop_words = True
    output_filename = "data_processed.csv"

# output_filename = "data_processed_train.csv"
# lemmatizing = True
# remove_stop_words = True

data_path = os.path.join("..", "data", "csv")
df = pd.read_csv(os.path.join(data_path, "data.csv"))

df['text'] = df.apply(format_text, axis=1)

df.to_csv(os.path.join(data_path, output_filename), index=False)

print("Finish preprocessing...")
print("Your processed data can be found in: " + os.path.abspath(os.path.join(data_path, output_filename)))

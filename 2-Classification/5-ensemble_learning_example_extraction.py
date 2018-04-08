import pandas as pd
import numpy as np
import os
import glob

categories = ["business", "entertainment", "politics", "sport", "technology"]


def convert_category_to_number(row):
    category = row['category']
    if category == 'business': return 1
    if category == "entertainment": return 2
    if category == "politics": return 3
    if category == "sport": return 4
    return 5


def convert_category_to_string(row, method):
    return categories[row[method] - 1]


def is_example(row):
    knn = row['predicted_k_nearest_neighbors']
    svm = row['predicted_support_vector_machine']
    dt = row['predicted_decision_tree']

    if knn == svm and svm == dt:
        return False
    if (knn - svm) * (svm - dt) * (dt - knn) == 0:
        return True
    return False


data_folder = os.path.join("..", "data")

df = pd.read_csv(os.path.join(data_folder, "csv", "data_processed_test.csv"))
df['category_number'] = df.apply(convert_category_to_number, axis=1)

predicted_files = glob.glob(os.path.join(data_folder, "npy", "predicted*"))
for predicted_file in predicted_files:
    method = predicted_file.split(os.sep)[-1].replace(".npy", "").replace(" ", "_").lower()
    df[method] = np.load(predicted_file)
    df[method.replace("predicted", "category")] = df.apply(convert_category_to_string, axis=1, args=(method,))

print(df.columns)

df['is_example'] = df.apply(is_example, axis=1)
df = df[df['is_example'] == True][['id', 'url', 'text', 'category', 'category_decision_tree',
                                   'category_k_nearest_neighbors', 'category_support_vector_machine',
                                   'category_ensemble_learning']]
df.to_csv(os.path.join(data_folder, "csv", "ensemble_examples.csv"), index=False)


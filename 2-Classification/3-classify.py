import pickle

import os


filename = input("Enter the pkl file name without .pkl: ")
data_folder = os.path.join("..", "data")

tfidf = pickle.load(open(os.path.join(data_folder, "pkl", filename + ".pkl"), "rb"))
print(tfidf.shape)


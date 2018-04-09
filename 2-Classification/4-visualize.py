from decouple import config
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import os

data_folder = os.path.join(config("DATA_FOLDER"), "npy")
filename = input("Enter the name of confusion matrix .npy file (with .npy): ")
confusion_matrix = np.load(os.path.join(data_folder, filename))

fig, ax = plot_confusion_matrix(conf_mat=confusion_matrix)
plt.suptitle(",".join(["0-business", "1-entertainment", "2-politics", "3-sport", "4-technology"]), fontsize=9)
print("Plotting confusion matrix for %s" % filename.replace(".npy", ""))
plt.show()

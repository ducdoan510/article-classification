from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import os

data_folder = os.path.join("..", "data", "npy")
filename = input("Enter the name of confusion matrix .npy file (with .npy): ")
confusion_matrix = np.load(os.path.join(data_folder, filename))

fig, ax = plot_confusion_matrix(conf_mat=confusion_matrix)
plt.show()

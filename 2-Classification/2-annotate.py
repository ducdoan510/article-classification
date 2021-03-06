import os
import pandas as pd
from decouple import config

csv_data_folder = os.path.join(config("DATA_FOLDER"), "csv")


def separate_data(filename):
    if not os.path.exists(os.path.join(csv_data_folder, filename + "_test.csv")):
        print("Annotated data does not exist...")
        print("Generating data containing 1000 records for annotating...")

        df = pd.read_csv(os.path.join(csv_data_folder, filename + ".csv"))

        test_data = df.sample(frac=0.1)
        test_data.to_csv(os.path.join(csv_data_folder, filename + "_test.csv"), index=False)
        print(test_data.shape)

        train_data = df.loc[~df.index.isin(test_data.index)]
        train_data.to_csv(os.path.join(csv_data_folder, filename + "_train.csv"), index=False)
        print(train_data.shape)

        print("Generated data containing 1000 records for annotating...")
        print("Please annotate the data before continue...Annotated data can be found at " +
              os.path.join(csv_data_folder, filename + "_test.csv"))

    else:
        print("File %s existed..." % os.path.join(csv_data_folder, filename + "_test.csv"))

separate_data("data_lowercase")
separate_data("data_processed")

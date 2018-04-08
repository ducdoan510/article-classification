import os
import pandas as pd


csv_data_folder = os.path.join("..", "data", "csv")
filename = input("Enter csv data file without .csv: ")

if not os.path.exists(os.path.join(csv_data_folder, filename + "_annotated.csv")):
    print("Annotated data does not exist...")
    print("Generating data containing 1000 records for annotating...")

    df = pd.read_csv(os.path.join(csv_data_folder, filename + ".csv"))

    df.sample(frac=0.1).to_csv(os.path.join(csv_data_folder, filename + "_annotated.csv"), index=False)

    print("Generated data containing 1000 records for annotating...")
    print("Please annotate the data and run the script again...Annotated data can be found at " +
          os.path.join(csv_data_folder, filename + "_annotated.csv"))
else:
    print("Annotated data exists...")
    print("Updating record category with annotated data...")

    original = pd.read_csv(os.path.join(csv_data_folder, filename + ".csv"))
    annotated = pd.read_csv(os.path.join(csv_data_folder, filename + "_annotated.csv"))

    for index, row in annotated.iterrows():
        original.loc[row['id'], 'category'] = row['category']

    original.to_csv(os.path.join(csv_data_folder, filename + ".csv"), index=False, encoding='utf-8')

    print("Done. Updated data can be found at " + os.path.join(csv_data_folder, filename + ".csv"))

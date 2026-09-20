import pandas as pd
import os

files = [
    "cooling_tower_dataset.csv",
    "dcgm.csv",
    "final_dataset_std.csv",
    "schedular_data.csv"
]

for file in files:
    path = "ml/data/raw/" + file

    if not os.path.exists(path):
        print("\n❌ FILE NOT FOUND:", file)
        continue

    if file == "final_dataset_std.csv":
        df = pd.read_csv(path, sep=";")
    else:
        df = pd.read_csv(path)

    print("\n==============================")
    print(file)
    print("Shape:", df.shape)
    print("Columns:")
    print(list(df.columns))
    print("==============================")




df = pd.read_csv(
    "ml/data/raw/cooling_tower_dataset.csv"
)

print("Shape:", df.shape)

print("\n===== COLUMNS =====")
print(df.columns.tolist())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATES =====")
print(df.duplicated().sum())

print("\n===== NUMERICAL SUMMARY =====")
print(df.describe())
 

 
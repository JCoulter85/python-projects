import pandas as pd

# Load the dataset
data = pd.read_csv("F:/Coding/Active_Businesses_-_County_Data.csv", encoding="utf-8")

# display the first few rows
print (data.head())

# display column names
print("Column Names:")
print(data.columns)

# check data structure and types
print("\nData information:")
print(data.info())

#check for missing values
print("\nMissing Values:")
print(data.isnull().sum())

# basic statistics for numeric columns
print("\nBasic Statistics:")
print(data.describe())

# unique values in each column
for col in data.columns:
        print(f"{col}: {data[col].nunique()} unique values")
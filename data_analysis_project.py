import pandas as pd
import matplotlib.pyplot as plt

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
        
# summary statistics for numeric columns
print("\nSummary Statistics:")
print(data.describe())

# count unique values in categorical columns
for col in data.select_dtypes(include=['object']).columns:
    print(f"{col}: {data[col].nunique()} unique values")
    
businesses_by_county = data.groupby('PPB County')['Business Name'].count()
print("\nBusinesses by County:")
print(businesses_by_county)

# avg_revenue_by_type = data.groupby('business_type')['revenue'].mean()
# print("\nAverage Revenue by Business Type:")
# print(avg_revenue_by_type)

# sort by the number of businesses in descending order
businesses_by_county = businesses_by_county.sort_values(ascending=False)
print("\nBusinesses by County (Sorted):")
print(businesses_by_county)

# Save the insights
businesses_by_county.to_csv("businesses_by_county.csv")

# bar chart of businesses by county
businesses_by_county.plot(kind='bar', figsize=(12,6), title="Businesses by County")
plt.xlabel("County")
plt.ylabel("Number of Businesses")
plt.tight_layout()
plt.show()

# top ten counties
top_10_counties = businesses_by_county.head(10)

# bar chart for top 10 counties
top_10_counties.plot(kind='bar', figsize=(10,5), color='skyblue', title="Top 10 Counties by Number of Businesses")
plt.xlabel("County")
plt.ylabel("Number of Businesses")
plt.tight_layout()
plt.show()

# Save the full chart
plt.savefig("businesses_by_County_Chart.png")

# save the top 10 chart
plt.savefig("top_10_counties_chart.png")
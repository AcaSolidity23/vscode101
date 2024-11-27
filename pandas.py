# Your Python code goes here
import pandas as pd
# Load the Excel file
file_path = '22808 Rec test.xlsx'
df = pd.read_excel(file_path)

# Extract column J (index 9, since columns are 0-indexed)
column_j = df.iloc[:, 9]

# Remove non-numeric values and NaNs
column_j = pd.to_numeric(column_j, errors='coerce').dropna()

# Calculate the median and highest value
median_value = column_j.median()
highest_value = column_j.max()

# Print the results
print(f"The median of column J is: {median_value}")
print(f"The highest value in column J is: {highest_value}")

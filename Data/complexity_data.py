import pandas as pd

# Read the CSV files
df_cpi = pd.read_csv('filtered_data_cpi.csv', delimiter=';')
df_ms = pd.read_csv('filtered_data_ms.csv', delimiter=';')

# Get the number of rows and columns in each DataFrame
rows_cpi, cols_cpi = df_cpi.shape
rows_ms, cols_ms = df_ms.shape

print(f"Size of CPI data: {rows_cpi} rows x {cols_cpi} columns")
print(f"Size of Money Supply data: {rows_ms} rows x {cols_ms} columns")

# Check the complexity (granularity) of the data
cpi_granularity = pd.to_datetime(df_cpi['Date']).diff().min()
ms_granularity = pd.to_datetime(df_ms['Date']).diff().min()

print(f"Complexity (granularity) of CPI data: {cpi_granularity}")
print(f"Complexity (granularity) of Money Supply data: {ms_granularity}")

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

def perform_adf_test(data, column, num_lags):
    adf_results = []
    for lag in num_lags:
        adf_result = adfuller(data[column].dropna(), maxlag=lag)
        adf_results.append(adf_result[1])
    return adf_results

# File names
cpi_file = 'filtered_data_cpi.csv'
ms_file = 'filtered_data_ms.csv'

# Read the consumer price index data
cpi_data = pd.read_csv(cpi_file, delimiter=';')
cpi_data['Date'] = pd.to_datetime(cpi_data['Date'])
cpi_data.set_index('Date', inplace=True)

# Read the money supply data
money_supply_data = pd.read_csv(ms_file, delimiter=';')
money_supply_data['Date'] = pd.to_datetime(money_supply_data['Date'])
money_supply_data.set_index('Date', inplace=True)

# Calculate rate of inflation
cpi_data['Inflation'] = cpi_data['price_change'].pct_change() * 100

# Calculate growth rate of money supply
money_supply_data['GrowthRate'] = money_supply_data['MoneySupply'].pct_change() * 100

# Define the number of lags for ADF test
num_lags = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Perform ADF test on the inflation series
adf_results_inflation = perform_adf_test(cpi_data, 'Inflation', num_lags)

# Perform ADF test on the money supply growth rate series
adf_results_growth_rate = perform_adf_test(money_supply_data, 'GrowthRate', num_lags)

# Save ADF test results in a CSV file
adf_results_df = pd.DataFrame({'Lag': num_lags, 'Inflation': adf_results_inflation, 'GrowthRate': adf_results_growth_rate})
adf_results_df.to_csv('adf_results.csv', index=False)

# Visualize ADF test results
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
ax1 = axes[0]
ax1.plot(num_lags, adf_results_inflation, marker='o')
ax1.set_title('ADF Test - Inflation')
ax1.set_xlabel('Number of Lags')
ax1.set_ylabel('p-value')
ax1.axhline(y=0.05, color='r', linestyle='--')

ax2 = axes[1]
ax2.plot(num_lags, adf_results_growth_rate, marker='o')
ax2.set_title('ADF Test - Money Supply Growth Rate')
ax2.set_xlabel('Number of Lags')
ax2.set_ylabel('p-value')
ax2.axhline(y=0.05, color='r', linestyle='--')

# Adjust subplot spacing manually
fig.subplots_adjust(hspace=0.4)

# Display the plot
plt.show()

# Save the plot with transparent background
plt.savefig('ADF_test_results.png', transparent=True)

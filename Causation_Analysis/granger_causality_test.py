import pandas as pd
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Read the data from the csv files and process it
cpi_data = pd.read_csv('filtered_data_cpi.csv', sep=';')
cpi_data['Date'] = pd.to_datetime(cpi_data['Date'])
cpi_data.set_index('Date', inplace=True)

money_supply_data = pd.read_csv('filtered_data_ms.csv', sep=';')
money_supply_data['Date'] = pd.to_datetime(money_supply_data['Date'])
money_supply_data.set_index('Date', inplace=True)

cpi_data['Inflation_Rate'] = cpi_data['price_change'].pct_change() * 100
money_supply_data['MoneySupply_Growth'] = money_supply_data['MoneySupply'].pct_change() * 100

merged_data = cpi_data.merge(money_supply_data, left_index=True, right_index=True)
merged_data.dropna(inplace=True)

def check_stationarity(series, name):
    result = adfuller(series)
    print(f"Results of ADF test for {name}")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Stationary" if result[1] < 0.05 else "Non-Stationary")
    print("")

# Check stationarity of inflation rate and money supply growth
check_stationarity(merged_data['Inflation_Rate'], "Inflation Rate")
check_stationarity(merged_data['MoneySupply_Growth'], "Money Supply Growth")

## Perform the Granger causality test on stationary series

# Extract the stationary series
stationary_data = merged_data[['MoneySupply_Growth', 'Inflation_Rate']].dropna()

# Define the maximum lag for the test (in our case: 10)
max_lag = 10

# Create lists to store the lag lengths and corresponding p-values
lag_lengths = []
p_values = []

# Iterate over the lag lengths
for lag in range(1, max_lag + 1):
    # Run the Granger causality test
    results = grangercausalitytests(merged_data[['MoneySupply_Growth', 'Inflation_Rate']].dropna(), maxlag=lag)
    # Extract the p-value for the lag
    p_value = results[lag][0]['ssr_chi2test'][1]
    # Store the lag length and p-value
    lag_lengths.append(lag)
    p_values.append(p_value)

# Set up the figure
fig, ax = plt.subplots()
ax.set_xlabel('Lag Length')
ax.set_ylabel('Granger Causality p-value')
ax.set_title('Sensitivity Analysis: Lag Length vs Granger Causality')

# Initialize the line plot
line, = ax.plot([], [], marker='o')

# Set the total number of frames and frame delay
total_frames = len(lag_lengths)
frame_delay = 200

# Function to update the line plot for each frame of the animation
def update(frame):
    line.set_data(lag_lengths[:frame + 1], p_values[:frame + 1])
    ax.set_xlim(1, frame + 1)
    ax.set_ylim(0, max(p_values[:frame + 1]) + 0.05)
    return line,

# Function to initialize the line plot
def init():
    line.set_data([], [])
    return line,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True)

# Save the animation as an animated GIF with a transparent background
ani.save('granger_causality_animation.gif', writer='pillow', dpi=300, 
         fps=1000/frame_delay, bitrate=3000)

# Print the lag lengths and corresponding p-values
for lag, p_value in zip(lag_lengths, p_values):
    print(f"Lag Length: {lag}, p-value: {p_value}")

# Finally, show the plot
plt.show()

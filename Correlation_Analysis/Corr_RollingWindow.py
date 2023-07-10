import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Read the data from CSV files
cpi_data = pd.read_csv('filtered_data_cpi.csv', delimiter=';')
money_supply_data = pd.read_csv('filtered_data_ms.csv', delimiter=';')

# Convert the date column to a datetime type
cpi_data['Date'] = pd.to_datetime(cpi_data['Date'])
money_supply_data['Date'] = pd.to_datetime(money_supply_data['Date'])

# Sort the data by monthly date
cpi_data = cpi_data.sort_values('Date')
money_supply_data = money_supply_data.sort_values('Date')

# Calculate the rate of inflation and the growth rate of money supply
cpi_data['InflationRate'] = cpi_data['price_change'].pct_change()
money_supply_data['MoneySupplyChange'] = money_supply_data['MoneySupply'].pct_change()

# Create a list of dates for the rolling window
start_date = pd.to_datetime('2017-01-01')
end_date = pd.to_datetime('2023-01-01')
window_dates = pd.date_range(start=start_date, end=end_date, freq='3M')

# Calculate the rolling window correlation for each window size
rolling_corr_values = []
for window_date in window_dates:
    window_size = int((window_date - start_date).days / 30)  # Convert window size to number of periods
    rolling_corr = cpi_data['InflationRate'].rolling(window=window_size).corr(money_supply_data['MoneySupplyChange'])
    rolling_corr_values.append(rolling_corr)

# Create the figure and subplots
fig, ax = plt.subplots(figsize=(12, 6))

# Set up an empty line for the animation
line, = ax.plot([], [], label='Rolling Window Correlation')

# Set the plot title, x-label, y-label, and legend
ax.set_title('Rolling Window Correlation')
ax.set_xlabel('Date')
ax.set_ylabel('Correlation')
ax.axhline(y=0, color='k', linestyle='--')
ax.legend()

# Function to update the line data for each frame of the animation
def update(frame):
    line.set_data(rolling_corr_values[frame].index, rolling_corr_values[frame])
    ax.set_xlim(rolling_corr_values[frame].index[0], rolling_corr_values[frame].index[-1])

# Create the animation using the FuncAnimation command
ani = animation.FuncAnimation(fig, update, frames=len(rolling_corr_values), interval=500)

# Save the animation as a video with transparent background using transparent = TRUE
ani.save('rolling_corr_animation.mp4', writer='imagemagick', dpi=300, transparent=True)
plt.close()

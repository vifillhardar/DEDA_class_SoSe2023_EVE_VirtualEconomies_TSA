import csv

# Open the CSV file and read the data
with open('money_supply.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    header = next(reader)
    data = list(reader)

# Filter the data to keep only the first day of each month
filtered_data = [data[0]] 

for i in range(1, len(data)):
    # Extract the year and month from the date
    current_date = data[i][0]
    current_year, current_month, _ = current_date.split('-')

    # Extract the year and month from the previous date
    previous_date = data[i-1][0]
    previous_year, previous_month, _ = previous_date.split('-')

    # Check if the current date is the first day of the month
    if current_year != previous_year or current_month != previous_month:
        filtered_data.append(data[i])

# Write the filtered data to a new CSV file
with open('filtered_data_ms.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(header)
    writer.writerows(filtered_data)

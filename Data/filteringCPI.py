import csv

# Open the input CSV file and read the data
with open('economy_indices_details.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Filter the data based on primary_index and sub_index
filtered_data = [(row['history_date'], row['price_change']) for row in data if row['primary_index'] == 'Consumer Price Index' and row['sub_index'] == 'Commodity']

# Write the filtered data to a new CSV file with ';' delimiter
fieldnames = ['Date', 'price_change']
with open('filtered_data_cpi.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for date, price_change in filtered_data:
        writer.writerow({'Date': date, 'price_change': price_change})

import requests
import zipfile

def download_and_extract_zip(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('data.zip', 'wb') as file:
            file.write(response.content)
            print('Zip file downloaded successfully.')

        with zipfile.ZipFile('data.zip', 'r') as zip_ref:
            zip_ref.extractall('extracted_data')
            print('Zip file extracted successfully.')
    else:
        print('Failed to download the zip file.')

def generate_monthly_url(month):
    url_template = "https://web.ccpgamescdn.com/aws/community/EVEOnline_MER_{}.zip"
    return url_template.format(month)

# Prompt the user to enter the month
month = input("Enter the month as 'Month20XX' (e.g. 'Mar2023'): ")

# Generate the monthly URL based on user input
url = generate_monthly_url(month)
download_and_extract_zip(url)

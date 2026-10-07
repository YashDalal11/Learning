import requests
import bs4
import pandas as pd
     
# Function to make HTTP GET request
def get_request(url, cookies={}, headers={}):
    return requests.get(url, cookies=cookies, headers=headers)


# Function to collect data from a URL and extract the table
def collect_data(url):
    response = get_request(url)
    soup = bs4.BeautifulSoup(response.text, features="lxml")
    table = soup.find("table", class_="publicholidays")
    return table


# Function to convert HTML table to pandas DataFrame
def convert_html_table_to_df(html_text):
    return pd.read_html(str(html_text))[0]


# Root URL for the website containing holiday data
ROOT_URL = "https://publicholidays.ae/2023-dates/"

# Collect the data and convert it to a DataFrame
html_text = collect_data(url=ROOT_URL)
df = convert_html_table_to_df(html_text=html_text)

# Save the DataFrame to a CSV file
df.iloc[:-1, :].to_csv("uae_holidays.csv")
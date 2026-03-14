import os
import requests
from dotenv import load_dotenv
import pandas as pd

# Load .env variables
load_dotenv()

API_KEY = os.getenv("EIA_API_KEY")

url = "https://api.eia.gov/v2/electricity/retail-sales/data/"

params = {
    "api_key": API_KEY,
    "frequency": "monthly",
    "data[0]": "customers",
    "data[1]": "price",
    "data[2]": "revenue",
    "data[3]": "sales",
    "facets[stateid][]": "CO",
    "start": "2023-01",
    "end": "2025-01",
    "offset": 0,
    "length": 5000
}

response = requests.get(url, params=params)

data = response.json()

# Convert to dataframe
df = pd.DataFrame(data["response"]["data"])

df.to_csv("C:\\Users\\neeva\\Documents\\00_Projects\\load-forecasting\\data\\raw\\retail_sales.csv")

print(df.head())
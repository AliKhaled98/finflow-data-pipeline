import os
import requests 
import pandas as pd
import pyarrow.parquet as pq
from dotenv import load_dotenv


load_dotenv()
APIKEY = os.getenv("ALPHA_VINTAGE_API_KEY")
BASE_URL = os.getenv("BASE_URL")

def fetch_api_data(from_currency, to_currency):

    parameters = {
        "function":   'CURRENCY_EXCHANGE_RATE',
        "from_currency":  from_currency,
        "to_currency":  to_currency,    
        "apikey": APIKEY

    }

    response = requests.get(BASE_URL, params=parameters)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None
    

exchange_data = fetch_api_data("EUR", "USD")

# View the raw JSON dictionary
# print(exchange_data)

dict_data = exchange_data['Realtime Currency Exchange Rate']
df = pd.DataFrame([dict_data])

df['ingested_at'] = pd.Timestamp.now()
df['Source'] = 'AlphaVantage'

map = {
    '1. From_Currency Code' : 'from_currency',
    '3. To_Currency Code' : 'to_currency',
    '5. Exchange Rate' : 'exchange_rate',
    '6. Last Refreshed' : 'last_refreshed',
}

df = df.rename(columns=map) 
crucial_cols = ['from_currency', 'to_currency', 'exchange_rate', 'last_refreshed', 'ingested_at', 'Source']
df = df[crucial_cols]

print(df.head())

storage_path = 'data/bronze/fx_rates'
os.makedirs(storage_path, exist_ok=True)

timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
data1 = f"{storage_path}/fx_eur_usd_{timestamp}.parquet"


df.to_parquet(data1, index=False)
print(f"Data successfully landed in Bronze: {data1}")
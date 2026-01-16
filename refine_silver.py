import glob
import pandas as pd
import os

def get_latest_file(path_pattern):

    files = glob.glob(path_pattern)
    if not files:
        return None
    
    files.sort()
    return files[-1]


API_path = 'data\\bronze\\fx_rates\\*.parquet'
scraped_path = 'data\\bronze\\market_scraped\\*.parquet'

latest_API = get_latest_file(API_path)
latest_scraped = get_latest_file(scraped_path)

if latest_API and latest_scraped:

    df_api = pd.read_parquet(latest_API)
    df_scraped = pd.read_parquet(latest_scraped)


df_api.rename(columns={'exchange_rate': 'api_rate', 'ingested_at': 'api_ingested_at', 'Source': 'api_source'}, inplace=True)
df_scraped.rename(columns={'scraped_price': 'market_rate', 'ingested_at': 'market_ingested_at', 'Source': 'market_source'}, inplace=True)


print(df_api.columns)
print('---------')
print(df_scraped.columns)

df_api['api_rate'] = df_api['api_rate'].astype(float)
df_api.info()

df = pd.merge(df_api, df_scraped, how='inner', left_on=['from_currency', 'to_currency'], right_on=['from_currency', 'to_currency'])
df['variance'] = df['market_rate'] - df['api_rate'] 
print(df.columns)

cols = ['from_currency', 'to_currency', 'api_rate', 'market_rate', 'variance', 'api_ingested_at', 'market_ingested_at', 'api_source', 'market_source']
df = df[cols]


# Use only relative paths to stay safe on Windows
storage_path = "data\\silver" 
os.makedirs(storage_path, exist_ok=True)

timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
filename = f"fx_hybrid_{timestamp}.parquet"


data2 = os.path.join(storage_path, filename)

df.to_parquet(data2, index=False)
print(f" Clean path created: {data2}")

print(df['variance'])
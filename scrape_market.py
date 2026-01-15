import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

def scrape_market_data():
    URL = 'https://finance.yahoo.com/quote/EURUSD=X/'
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup
    else:
        print('Access Denied')
        return None
    
soup_obj = scrape_market_data()
if soup_obj:
    print('Successfully caught the soup!')


def extract_exchange_rate(soup):
    price_tag = soup.find(attrs={'data-testid': 'qsp-price'})

    if price_tag:
        return price_tag.text
    
    return None 

if soup_obj:
    price = extract_exchange_rate(soup_obj)

    if price:

        data={
            'from_currency': 'EUR',
            'to_currency': 'USD',
            'scraped_price': float(price.replace(',', '')),
            'ingested_at': pd.Timestamp.now(),
            'Source': 'YahooFinance_Scraper'
        }

    df = pd.DataFrame([data])

    storage_path = 'data/bronze/market_scraped'
    os.makedirs(storage_path, exist_ok=True)

    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    scraped_data = f'{storage_path}/fx_market_{timestamp}.parquet'

    df.to_parquet(scraped_data, index=False)
    print(f'Market data saved: {scraped_data}')

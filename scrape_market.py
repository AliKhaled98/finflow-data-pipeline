import yfinance as yf
import pandas as pd
import os

def get_market_data():
    # The ticker for USD to EGP on Yahoo Finance is "USDEGP=X"
    ticker_symbol = "USDEGP=X"
    
    try:
        # Fetch data using the yfinance Ticker object
        ticker = yf.Ticker(ticker_symbol)
        
        # fast_info provides the most recent live data point
        price = ticker.fast_info['last_price']
        
        if price:
            return {
                'from_currency': 'USD',
                'to_currency': 'EGP',
                'scraped_price': float(price),
                'ingested_at': pd.Timestamp.now(),
                'Source': 'yfinance_API'
            }
    except Exception as e:
        print(f" Error fetching data: {e}")
    return None

# --- Process and Save ---
market_data = get_market_data()

if market_data:
    df = pd.DataFrame([market_data])

    # Path safety for your D: drive project folder
    storage_path = os.path.join('data', 'bronze', 'market_scraped')
    os.makedirs(storage_path, exist_ok=True)

    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    filename = f'fx_market_{timestamp}.parquet'
    save_path = os.path.join(storage_path, filename)

    df.to_parquet(save_path, index=False)
    
    print(f" Success! USD/EGP Market Price: {market_data['scraped_price']}")
    print(f" Saved to: {save_path}")
else:
    print(" Failed to retrieve market data.")
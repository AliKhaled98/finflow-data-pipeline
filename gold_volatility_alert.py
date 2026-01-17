"""
Gold Layer: Business Intelligence & Risk Alerting.
- Calculates Spread Percentage KPI.
- Flags high volatility based on a risk threshold.
- Saves a final 'Fact Table' for reporting.
"""
import glob
import pandas as pd
import os

def get_latest_file(path_pattern):
    files = glob.glob(path_pattern)
    if not files:
        return None
    files.sort()
    return files[-1]

# 1. LOAD SILVER DATA
silver_path = os.path.join('data', 'silver', '*.parquet')
latest_silver = get_latest_file(silver_path)

if latest_silver:
    df = pd.read_parquet(latest_silver)
    
    # 2. KPI GENERATION
    df['absolute_variance'] = df['variance'].abs()
    df['spread_percentage'] = (df['absolute_variance'] / df['api_rate']) * 100

    # 3. RISK MONITORING
    risk_threshold = 0.1
    df['is_high_volatility'] = df['spread_percentage'] > risk_threshold

    # 4. DATA CURATION
    gold_cols = ['from_currency', 'to_currency', 'api_rate', 'market_rate', 'absolute_variance', 'spread_percentage', 'is_high_volatility', 'api_ingested_at']
    df_gold = df[gold_cols].copy()

    # 5. PERSISTENCE
    gold_path = os.path.join('data', 'gold')
    os.makedirs(gold_path, exist_ok=True)
    
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(gold_path, f"fact_fx_volatility_{timestamp}.parquet")
    df_gold.to_parquet(filename, index=False)

    # 6. ACTIONABLE OUTPUT
    print('-'*30)
    print(f'Gold volatility alert created: {filename}')
    
    if df_gold['is_high_volatility'].any():
        print('Alert: Significant USD/EGP Volatility Detected')
        print(f"USD/EGP Spread is {df_gold['spread_percentage'].iloc[0]:.4f}%!")
        print('Action: Advise Finance Team to delay non-essential USD transactions')
    else:
        print(f'Market stable: Spread is within safe limits ({df_gold["spread_percentage"].iloc[0]:.4f}%)')    
    print('-'*30)

else:
    print('No silver data file found')
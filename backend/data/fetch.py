import pandas as pd
import yfinance as yf
import os

def fetch_stock_data(ticker, period="5y"):
    os.makedirs(f'backend/data', exist_ok=True)
    cache_path = f'backend/data/{ticker}.csv'
    
    if os.path.exists(cache_path):
        return pd.read_csv(cache_path, index_col=0, parse_dates=True)
    
    df = yf.download(ticker, period=period)
    df.columns = df.columns.droplevel(1)
    df.dropna(inplace=True)
    df.to_csv(cache_path)
    return df


if __name__ == "__main__":
    df = fetch_stock_data("AAPL")
    print(df.tail(5)) 


import numpy as np
from backend.data import fetch
def moving_average_crossover(df, short_window=20, long_window=50):
    df['stma'] = df['Close'].rolling(window=short_window).mean()
    df['ltma'] = df['Close'].rolling(window=long_window).mean()

    df['Signal'] = np.where(
        df['stma'] > df['ltma'], 1, 
        np.where(df['stma'] < df['ltma'],  -1 , 0),) 
    
    return df

if __name__ == "__main__":
    df = fetch.fetch_stock_data("AAPL")
    result = moving_average_crossover(df)
    print(result[['Close', 'stma', 'ltma', 'Signal']].tail(20))
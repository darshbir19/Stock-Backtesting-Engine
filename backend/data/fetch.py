import pandas as pd
import yfinance as yf
import os


def fetch_stock_data(ticker, period="5y"):

    # if os.path.exists(f'backend/data/{ticker}.csv'):
        df = pd.read_csv(f'backend/data/{ticker}.csv')
    # else:
        df = yf.download(ticker , period = period)
        df.dropna(inplace=True) # Drops invalid NaN values: for days when market hasnt closed or it is a holiday.
        # df.to_csv(f'backend/data/{ticker}.csv')
        return df



if __name__ == "__main__":
    df = fetch_stock_data("AAPL")
    print(df.tail(5)) 


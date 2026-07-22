import pandas as pd
import yfinance as yf
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def fetch_stock_data(ticker, period="5y"):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT ticker, date, open, high, low, close, volume FROM prices WHERE ticker = %s ORDER BY date", (ticker,))
    rows = cursor.fetchall()
    
    if rows:
        cursor.close()
        conn.close()
        df = pd.DataFrame(rows, columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])
        df.set_index('date', inplace=True)
        df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
        return df
    
    df = yf.download(ticker, period=period)
    df.columns = df.columns.droplevel(1)
    df.dropna(inplace=True)
    
    for date, row in df.iterrows():
        cursor.execute("""
            INSERT INTO prices (ticker, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (ticker, date.strftime('%Y-%m-%d'), 
              float(row['Open']), float(row['High']), 
              float(row['Low']), float(row['Close']), 
              int(row['Volume'])))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return df


if __name__ == "__main__":
    df = fetch_stock_data("AAPL")
    print(df.tail(5))
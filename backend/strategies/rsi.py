import numpy as np
from backend.data import fetch
def rsi(df , period = 14 , oversold=30, overbought=70):
    df['Change'] = df['Close'].diff()
    df['Gain'] = np.where(df['Change'] > 0,  df['Change'], 0)
    df['Loss'] = np.where(df['Change'] < 0,  df['Change'].abs() , 0)
    df['Avg_Gain'] = df['Gain'].rolling(window= period).mean()
    df['Avg_Loss'] = df['Loss'].rolling(window= period).mean()
    df["RS"] = df["Avg_Gain"] / df["Avg_Loss"]
    df['RSI'] = 100 - (100/ (1 + df['RS']))
    df['Signal'] = np.where(
        df['RSI'] > overbought, -1, 
        np.where(df['RSI'] < oversold , 1 , 0)) 
    
    return df
    

if __name__ == "__main__":
    df = fetch.fetch_stock_data("AAPL")
    result = rsi(df)
    print(result[['Avg_Gain', 'Avg_Loss' , 'RSI' , 'RSI_Signal']].tail(30))
    


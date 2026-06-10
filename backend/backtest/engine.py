
def run_backtest(df, initial_capital=10000.0): # signal is binary here for simplicity: we are either in the market or out of it, nothing in between.
    capital = initial_capital
    position = 0
    portfolio_list = []
    trade_list = []

    for i in df.index:
        if (df.at[i , 'Signal'] == 1 and position == 0):
            shares = capital/df.at[i, 'Close']
            capital = 0
            position = shares
            trade_list.append({"date": i, "type": "BUY", "price": df.at[i, "Close"]})
        elif (df.at[i , 'Signal'] == -1 and position > 0):
            
            capital = position*df.at[i, 'Close']
            position = 0
            trade_list.append({"date": i, "type": "SELL", "price": df.at[i, "Close"]})

        portfolio_value = capital + position*df.at[i, 'Close']
        portfolio_list.append(portfolio_value)
        
    return portfolio_list, trade_list

if __name__ == "__main__":
    from backend.data import fetch
    from backend.strategies import moving_average

    df = fetch.fetch_stock_data("AAPL")
    df = moving_average.moving_average_crossover(df)
    
    portfolio, trades = run_backtest(df)
    
    print(f"Starting capital: $10,000")
    print(f"Final value: ${portfolio[-1]:.2f}")
    print(f"Total trades: {len(trades)}")
    print(f"First 5 trades: {trades[:5]}")
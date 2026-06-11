from fastapi import FastAPI
from backend.data import fetch
from backend.strategies import moving_average , rsi
from backend.backtest import engine
from backend.metrics import calculator
app = FastAPI()

@app.get("/backtest")
def backtest(ticker: str, strategy: str):
    
    df = fetch.fetch_stock_data(ticker)
    if strategy == "moving_average":
        df = moving_average.moving_average_crossover(df)
    elif strategy == "rsi":
        df = rsi.rsi(df)
    portfolio_list, trade_list = engine.run_backtest(df)
    win_rate , mdd , sharpe_ratio = calculator.calculate_metrics(portfolio_list)
    final_value = portfolio_list[-1]
    return {                                             
    "final_value": final_value,
    "win_rate": win_rate,
    "max_drawdown": mdd,
    "sharpe_ratio": sharpe_ratio
}
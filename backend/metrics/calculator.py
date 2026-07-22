import numpy as np
import math
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

def calculate_metrics(portfolio_list):
    portfolio_arr = np.array(portfolio_list)
    daily_returns = np.diff(portfolio_arr)/portfolio_arr[:-1]

    win_mask = daily_returns > 0
    win_rate = np.sum(win_mask)/len(daily_returns)

    running_peak = np.maximum.accumulate(portfolio_arr)
    mdd = (running_peak - portfolio_arr)/running_peak
    mdd = np.max(mdd)
    if not np.isfinite(mdd):
        mdd = 0.0

    risk_free = 0.05/252
    excess_returns = daily_returns - risk_free
    mean_ex = np.mean(excess_returns)
    std_ex = np.std(excess_returns, ddof=1)

    if std_ex == 0:
        sharpe_ratio = 0.0
    else:
        sharpe_ratio = mean_ex / std_ex * math.sqrt(252)

    return win_rate, mdd, sharpe_ratio


def log_backtest_result(ticker, strategy, sharpe, mdd, win_rate, final_value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO backtest_results (ticker, strategy, sharpe_ratio, max_drawdown, win_rate, final_value)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (ticker, strategy, float(sharpe), float(mdd), float(win_rate), float(final_value)))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    from backend.data import fetch
    from backend.strategies import moving_average
    from backend.backtest.engine import run_backtest

    df = fetch.fetch_stock_data("AAPL")
    df = moving_average.moving_average_crossover(df)
    portfolio, trades = run_backtest(df)

    win_rate, mdd, sharpe = calculate_metrics(portfolio)

    print(f"Win Rate:      {win_rate*100:.2f}%")
    print(f"Max Drawdown:  {mdd*100:.2f}%")
    print(f"Sharpe Ratio:  {sharpe:.3f}")

    log_backtest_result("AAPL", "moving_average", sharpe, mdd, win_rate, portfolio[-1])
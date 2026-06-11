from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.data import fetch
from backend.strategies import moving_average , rsi
from backend.backtest import engine
from backend.metrics import calculator
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/backtest")
def backtest(ticker: str, strategy: str):
    
    df = fetch.fetch_stock_data(ticker)
    if strategy == "moving_average":
        df = moving_average.moving_average_crossover(df)
    elif strategy == "rsi":
        df = rsi.rsi(df)
    elif strategy == "lstm":
        try:
            from backend.ml.predict import generate_lstm_signals

            df = generate_lstm_signals(df)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
    else:
        raise HTTPException(status_code=400, detail=f"Unknown strategy: {strategy}")

    portfolio_list, trade_list = engine.run_backtest(df)
    portfolio_data = [{"day": i, "value": v} for i, v in enumerate(portfolio_list)]
    win_rate , mdd , sharpe_ratio = calculator.calculate_metrics(portfolio_list)
    final_value = portfolio_list[-1]
    return {                                             
    "final_value": final_value,
    "win_rate": win_rate,
    "max_drawdown": mdd,
    "sharpe_ratio": sharpe_ratio,
    "portfolio": portfolio_data
}

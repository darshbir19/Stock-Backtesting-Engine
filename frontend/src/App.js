import { useState } from "react"

function App() {
    const [ticker, setTicker] = useState("AAPL")
    const [strategy, setStrategy] = useState("moving_average")
    const [results, setResults] = useState(null)
    const [loading, setLoading] = useState(false)

    
    async function runBacktest() 
    {
      setLoading(true)
      const response = await fetch(`http://127.0.0.1:8000/backtest?ticker=${ticker}&strategy=${strategy}`)
      const data = await response.json();
      setResults(data)
      setLoading(false)
    }

    return (
        <div>
          <div>
            <label>Ticker:</label>
            <input 
                type="text" 
                value={ticker} 
                onChange={(e) => setTicker(e.target.value)}
            />
          </div>

          <div>
            <label>Strategy</label>
            <select 
                value={strategy}
                onChange={(e) => setStrategy(e.target.value)}>
                <option value="moving_average">Moving Average</option>
                <option value="rsi">RSI</option>
            </select>
          </div>

          <div>
            <button 
                type="button"
                onClick={() => runBacktest()}>Run Backtest</button>
          </div>

          {loading && <p>Loading...</p>}

          {results && (
            <div>
                <p>Final Value: ${results.final_value.toFixed(2)}</p>
                <p>Win Rate: {(results.win_rate * 100).toFixed(2)}%</p>
                <p>Max Drawdown: {(results.max_drawdown * 100).toFixed(2)}%</p>
                <p>Sharpe Ratio: {results.sharpe_ratio.toFixed(3)}</p>
            </div>
          )}
        </div>
    )
  }
            
        
export default App



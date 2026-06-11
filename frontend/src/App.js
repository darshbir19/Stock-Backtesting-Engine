import { useState } from "react"
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';

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
                <option value="lstm">LSTM</option>
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

                <div style={{width: "100%", minHeight: "400px"}}>
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart
            responsive
            data={results.portfolio}
            margin={{
              top: 5,
              right: 0,
              left: 0,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#8884d8" />
            <XAxis dataKey="day" stroke="#8884d8" />
            <YAxis width="auto" stroke="#8884d8" />
            <Tooltip
              cursor={{
                stroke: "#8884d8",
              }}
              contentStyle={{
                backgroundColor: 'var(--color-surface-raised)',
                borderColor: "#8884d8",
              }}
            />
            <Legend />  
            <Line
              type="monotone"
              dataKey="value"
              stroke="#8884d8"
              dot={
                false
              }
              activeDot={{ stroke: "#8884d8" }}
            />
          </LineChart>
          </ResponsiveContainer>  
          </div>
            </div>
          )}
        </div>
    )
  }
            
        
export default App



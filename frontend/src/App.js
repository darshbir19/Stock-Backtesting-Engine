import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

const strategies = [
  {
    value: "moving_average",
    label: "Moving Average",
    description: "Trend-following baseline for steadier entries.",
  },
  {
    value: "rsi",
    label: "RSI",
    description: "Momentum signal tuned for overbought and oversold swings.",
  },
  {
    value: "lstm",
    label: "LSTM",
    description: "Forecast-driven model for sequence-aware predictions.",
  },
];

const currencyFormatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

function formatPercent(value) {
  return `${(Number(value || 0) * 100).toFixed(2)}%`;
}

function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [strategy, setStrategy] = useState("moving_average");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const selectedStrategy = strategies.find((item) => item.value === strategy);

  async function runBacktest(event) {
    event.preventDefault();
    const normalizedTicker = ticker.trim().toUpperCase();

    if (!normalizedTicker) {
      setError("Enter a ticker symbol to run a backtest.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const params = new URLSearchParams({
        ticker: normalizedTicker,
        strategy,
      });
      const response = await fetch(`http://127.0.0.1:8000/backtest?${params}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.detail || "The backtest service returned an error."
        );
      }

      const data = await response.json();
      setTicker(normalizedTicker);
      setResults(data);
    } catch (err) {
      setError(err.message || "Unable to run the backtest.");
    } finally {
      setLoading(false);
    }
  }

  const metrics = results
    ? [
        {
          label: "Final Value",
          value: currencyFormatter.format(results.final_value || 0),
        },
        {
          label: "Win Rate",
          value: formatPercent(results.win_rate),
        },
        {
          label: "Max Drawdown",
          value: formatPercent(results.max_drawdown),
        },
        {
          label: "Sharpe Ratio",
          value: Number(results.sharpe_ratio || 0).toFixed(3),
        },
      ]
    : [];

  return (
    <main className="app-shell">
      <section className="dashboard">
        <header className="dashboard-header">
          <div>
            <p className="eyebrow">Strategy Workbench</p>
            <h1>Backtest trading ideas with clean performance context.</h1>
          </div>
          <div className="status-pill">
            <span className="status-dot" />
            API ready
          </div>
        </header>

        <div className="workspace-grid">
          <aside className="control-panel" aria-label="Backtest controls">
            <form onSubmit={runBacktest}>
              <div className="field-group">
                <label htmlFor="ticker">Ticker</label>
                <input
                  id="ticker"
                  type="text"
                  value={ticker}
                  placeholder="AAPL"
                  autoComplete="off"
                  onChange={(event) => setTicker(event.target.value)}
                />
              </div>

              <div className="field-group">
                <label htmlFor="strategy">Strategy</label>
                <select
                  id="strategy"
                  value={strategy}
                  onChange={(event) => setStrategy(event.target.value)}
                >
                  {strategies.map((item) => (
                    <option key={item.value} value={item.value}>
                      {item.label}
                    </option>
                  ))}
                </select>
                <p className="field-hint">{selectedStrategy?.description}</p>
              </div>

              <button className="primary-action" type="submit" disabled={loading}>
                {loading ? "Running..." : "Run Backtest"}
              </button>
            </form>

            {error && <p className="alert">{error}</p>}

            <div className="note-panel">
              <p>Selected Strategy</p>
              <strong>{selectedStrategy?.label}</strong>
            </div>
          </aside>

          <section className="results-panel" aria-live="polite">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Portfolio Equity</p>
                <h2>{results ? `${ticker} backtest` : "Run a backtest"}</h2>
              </div>
              {results && (
                <span className="strategy-badge">{selectedStrategy?.label}</span>
              )}
            </div>

            {results ? (
              <>
                <div className="metric-grid">
                  {metrics.map((metric) => (
                    <article className="metric-card" key={metric.label}>
                      <p>{metric.label}</p>
                      <strong>{metric.value}</strong>
                    </article>
                  ))}
                </div>

                <div className="chart-card">
                  <ResponsiveContainer width="100%" height={390}>
                    <LineChart
                      data={results.portfolio}
                      margin={{ top: 16, right: 24, left: 10, bottom: 12 }}
                    >
                      <CartesianGrid strokeDasharray="4 4" stroke="#d6dee8" />
                      <XAxis
                        dataKey="day"
                        stroke="#6b7280"
                        tickLine={false}
                        axisLine={false}
                      />
                      <YAxis
                        stroke="#6b7280"
                        tickLine={false}
                        axisLine={false}
                        width={72}
                        tickFormatter={(value) =>
                          currencyFormatter.format(value).replace(".00", "")
                        }
                      />
                      <Tooltip
                        formatter={(value) => [
                          currencyFormatter.format(value),
                          "Portfolio value",
                        ]}
                        labelFormatter={(value) => `Day ${value}`}
                        contentStyle={{
                          backgroundColor: "#ffffff",
                          border: "1px solid #dbe3ec",
                          borderRadius: "8px",
                          boxShadow: "0 18px 45px rgba(15, 23, 42, 0.12)",
                        }}
                      />
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#0f766e"
                        strokeWidth={3}
                        dot={false}
                        activeDot={{ r: 6, strokeWidth: 0, fill: "#0f766e" }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </>
            ) : (
              <div className="empty-state">
                <span />
                <h2>No results yet</h2>
                <p>Choose a ticker and strategy, then run a backtest.</p>
              </div>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}

export default App;

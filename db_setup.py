import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10),
    date DATE,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume BIGINT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS backtest_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10),
    strategy VARCHAR(50),
    sharpe_ratio FLOAT,
    max_drawdown FLOAT,
    win_rate FLOAT,
    final_value FLOAT,
    run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
print("Tables created successfully.")

cursor.close()
conn.close()
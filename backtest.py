import yfinance as yf

def run_silver_bullet_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1mo", interval="1h")
    
    balance = 1000.00
    risk = 20.00
    reward = 50.00 # 1:2.5 Ratio
    
    print("--- Testing Silver Bullet Methodology ---")
    
    for i in range(24, len(df) - 10):
        # Focus on London Session (approx 8:00 - 11:00 AM EAT)
        hour = df.index[i].hour
        if 8 <= hour <= 11:
            
            # Liquidity Sweep
            high_prev = df['High'].iloc[i-5:i].max()
            low_prev = df['Low'].iloc[i-5:i].min()
            
            # Strong Momentum Close
            body_size = abs(df['Close'].iloc[i] - df['Open'].iloc[i])
            
            if df['High'].iloc[i] > high_prev and df['Close'].iloc[i] < df['Open'].iloc[i]:
                # Sell Signal
                if df['Low'].iloc[i+1:i+6].min() < (df['Close'].iloc[i] - 0.0500):
                    balance += reward
                else:
                    balance -= risk
            
            elif df['Low'].iloc[i] < low_prev and df['Close'].iloc[i] > df['Open'].iloc[i]:
                # Buy Signal
                if df['High'].iloc[i+1:i+6].max() > (df['Close'].iloc[i] + 0.0500):
                    balance += reward
                else:
                    balance -= risk

    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_silver_bullet_backtest()

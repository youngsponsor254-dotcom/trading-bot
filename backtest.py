import yfinance as yf

def run_silver_bullet_optimized():
    ticker = yf.Ticker("GBPUSD=X")
    # Using 3 months of data to ensure the strategy is robust
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    
    print("--- Running Volatility-Adjusted Silver Bullet ---")
    
    for i in range(24, len(df) - 10):
        # London Session Filter (8 AM - 11 AM EAT)
        hour = df.index[i].hour
        if 8 <= hour <= 11:
            
            # Dynamic Volatility Filter (ATR-like logic)
            atr = df['High'].iloc[i-5:i].max() - df['Low'].iloc[i-5:i].min()
            sl_val = max(0.0020, atr * 1.5) # Minimum 20 pips, or 1.5x volatility
            tp_val = sl_val * 2.0           # 1:2 Risk-Reward
            
            high_prev = df['High'].iloc[i-5:i].max()
            low_prev = df['Low'].iloc[i-5:i].min()
            
            # Entry logic
            if df['High'].iloc[i] > high_prev and df['Close'].iloc[i] < df['Open'].iloc[i]:
                # Sell
                if df['Low'].iloc[i+1:i+6].min() < (df['Close'].iloc[i] - tp_val):
                    balance += (tp_val * 10000) * 0.10 # Simplified profit calc
                else:
                    balance -= (sl_val * 10000) * 0.10
            
            elif df['Low'].iloc[i] < low_prev and df['Close'].iloc[i] > df['Open'].iloc[i]:
                # Buy
                if df['High'].iloc[i+1:i+6].max() > (df['Close'].iloc[i] + tp_val):
                    balance += (tp_val * 10000) * 0.10
                else:
                    balance -= (sl_val * 10000) * 0.10

    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_silver_bullet_optimized()

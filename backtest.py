import yfinance as yf

def run_pure_silver_bullet():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    sl = 0.0020  # Fixed 20 pips
    tp = 0.0040  # Fixed 40 pips (1:2 RR)
    
    print("--- Running Pure Silver Bullet (Fixed 20/40) ---")
    
    for i in range(24, len(df) - 10):
        hour = df.index[i].hour
        # London Session Window
        if 8 <= hour <= 11:
            high_prev = df['High'].iloc[i-5:i].max()
            low_prev = df['Low'].iloc[i-5:i].min()
            
            # Entry: Liquidity Sweep
            if df['High'].iloc[i] > high_prev and df['Close'].iloc[i] < df['Open'].iloc[i]:
                # Sell
                if df['Low'].iloc[i+1:i+6].min() < (df['Close'].iloc[i] - tp):
                    balance += 40
                else:
                    balance -= 20
            
            elif df['Low'].iloc[i] < low_prev and df['Close'].iloc[i] > df['Open'].iloc[i]:
                # Buy
                if df['High'].iloc[i+1:i+6].max() > (df['Close'].iloc[i] + tp):
                    balance += 40
                else:
                    balance -= 20

    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_pure_silver_bullet()

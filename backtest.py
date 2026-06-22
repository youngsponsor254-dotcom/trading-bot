import yfinance as yf

def run_silver_bullet_1to2():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1mo", interval="1h")
    
    balance = 1000.00
    risk = 20.00
    reward = 40.00 # 1:2 Ratio
    
    print("--- Testing Silver Bullet 1:2 Strategy ---")
    
    for i in range(24, len(df) - 10):
        # London Session (8 AM - 11 AM EAT)
        hour = df.index[i].hour
        if 8 <= hour <= 11:
            
            # Liquidity Sweep (Highs/Lows of previous 5 hours)
            high_prev = df['High'].iloc[i-5:i].max()
            low_prev = df['Low'].iloc[i-5:i].min()
            
            # Entry logic: Sweep + Close back inside
            if df['High'].iloc[i] > high_prev and df['Close'].iloc[i] < df['Open'].iloc[i]:
                # Sell: Target 40 pips profit, 20 pips loss
                if df['Low'].iloc[i+1:i+6].min() < (df['Close'].iloc[i] - 0.0040):
                    balance += reward
                else:
                    balance -= risk
            
            elif df['Low'].iloc[i] < low_prev and df['Close'].iloc[i] > df['Open'].iloc[i]:
                # Buy: Target 40 pips profit, 20 pips loss
                if df['High'].iloc[i+1:i+6].max() > (df['Close'].iloc[i] + 0.0040):
                    balance += reward
                else:
                    balance -= risk

    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_silver_bullet_1to2()

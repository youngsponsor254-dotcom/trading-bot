import yfinance as yf

def run_original_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    risk = 10.00
    reward = 20.00 # 1:2 Reward
    
    print("--- Testing Original 47% Win Rate Logic ---")
    
    for i in range(200, len(df) - 10):
        ema200 = df['Close'].iloc[i-200:i].mean()
        
        # Original FVG/Sweep logic (Simple)
        fvg_low = float(df['Low'].iloc[i-3])
        fvg_high = float(df['High'].iloc[i-2])
        is_fvg = fvg_low > fvg_high
        
        # Simple directional logic
        if df['Close'].iloc[i] < ema200 and is_fvg:
            # Sell: Does it drop 0.2%?
            if df['Low'].iloc[i+1:i+8].min() < (df['Close'].iloc[i] * 0.998):
                balance += reward
            else:
                balance -= risk
        
        elif df['Close'].iloc[i] > ema200 and is_fvg:
            # Buy: Does it rise 0.2%?
            if df['High'].iloc[i+1:i+8].max() > (df['Close'].iloc[i] * 1.002):
                balance += reward
            else:
                balance -= risk
                
    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_original_backtest()

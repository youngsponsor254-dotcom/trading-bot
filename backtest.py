import yfinance as yf

def run_profit_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    # Using 3 months of data for a robust sample size
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    risk_per_trade = 10.00
    
    print("--- Starting 1:2 Tuned Backtest ---")
    
    for i in range(200, len(df) - 10):
        # 1. Trend Filter: EMA 200
        ema200 = df['Close'].iloc[i-200:i].mean()
        is_bearish = df['Close'].iloc[i] < ema200
        is_bullish = df['Close'].iloc[i] > ema200
        
        # 2. Rule: Precision Liquidity Sweep (12h Lookback)
        swing_low = df['Low'].iloc[i-12:i].min()
        swing_high = df['High'].iloc[i-12:i].max()
        
        is_bullish_sweep = df['Low'].iloc[i] < swing_low and df['Close'].iloc[i] > swing_low
        is_bearish_sweep = df['High'].iloc[i] > swing_high and df['Close'].iloc[i] < swing_high
        
        # 3. Execution (1:2 Risk Reward)
        if is_bearish and is_bearish_sweep:
            # Target 0.2% drop within 8 hours
            if df['Low'].iloc[i+1:i+8].min() < (df['Close'].iloc[i] * 0.998):
                balance += 20.00 # Win $20
            else:
                balance -= 10.00 # Loss $10
        
        elif is_bullish and is_bullish_sweep:
            # Target 0.2% rise within 8 hours
            if df['High'].iloc[i+1:i+8].max() > (df['Close'].iloc[i] * 1.002):
                balance += 20.00 # Win $20
            else:
                balance -= 10.00 # Loss $10
                
    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_profit_backtest()

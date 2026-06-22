import yfinance as yf

def run_high_probability_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    risk = 20.00   # 20 pips SL
    reward = 60.00 # 60 pips TP (1:3 ratio)
    
    print("--- Running High-Probability 1:3 Backtest ---")
    
    for i in range(200, len(df) - 36):
        ema200 = df['Close'].iloc[i-200:i].mean()
        
        # Identify FVG: The gap between candle i-3 and i-1
        fvg_detected = (df['Low'].iloc[i-1] > df['High'].iloc[i-3])
        
        # Entry Logic: Trend + FVG + Price Touch
        if df['Close'].iloc[i] > ema200 and fvg_detected:
            # Buy setup
            # Did it hit +60 pips before -20 pips?
            if df['High'].iloc[i+1:i+36].max() > (df['Close'].iloc[i] + 0.0060):
                balance += reward
            else:
                balance -= risk
                
        elif df['Close'].iloc[i] < ema200 and fvg_detected:
            # Sell setup
            if df['Low'].iloc[i+1:i+36].min() < (df['Close'].iloc[i] - 0.0060):
                balance += reward
            else:
                balance -= risk
                
    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_high_probability_backtest()

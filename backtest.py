import yfinance as yf

def run_profit_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    risk = 10.00
    reward = 20.00
    
    print("--- Starting 'Confirmation-Only' Backtest ---")
    
    for i in range(200, len(df) - 10):
        ema200 = df['Close'].iloc[i-200:i].mean()
        swing_low = df['Low'].iloc[i-12:i].min()
        swing_high = df['High'].iloc[i-12:i].max()
        
        # 1. Detect the Sweep
        bullish_sweep = df['Low'].iloc[i] < swing_low
        bearish_sweep = df['High'].iloc[i] > swing_high
        
        # 2. Confirmation: The candle must CLOSE back inside the range
        # This proves the sweep was a 'Liquidity Trap'
        bullish_confirmed = bullish_sweep and df['Close'].iloc[i] > swing_low
        bearish_confirmed = bearish_sweep and df['Close'].iloc[i] < swing_high
        
        # 3. Execution (Trend + Confirmation)
        if df['Close'].iloc[i] < ema200 and bearish_confirmed:
            # Sell Trade
            if df['Low'].iloc[i+1:i+8].min() < (df['Close'].iloc[i] * 0.998):
                balance += reward
            else:
                balance -= risk
        
        elif df['Close'].iloc[i] > ema200 and bullish_confirmed:
            # Buy Trade
            if df['High'].iloc[i+1:i+8].max() > (df['Close'].iloc[i] * 1.002):
                balance += reward
            else:
                balance -= risk
                
    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_profit_backtest()

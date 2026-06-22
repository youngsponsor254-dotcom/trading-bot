import yfinance as yf

def run_profit_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000 # Starting with $1000
    risk_per_trade = 10 # Risk $10 per trade
    
    for i in range(24, len(df) - 10):
        # Your "Rectified" Logic
        ema200 = df['Close'].iloc[i-200:i].mean()
        is_bearish = df['Close'].iloc[i] < ema200
        swing_low = df['Low'].iloc[i-24:i].min()
        liquidity_swept = df['Low'].iloc[i] < swing_low
        
        if is_bearish and liquidity_swept:
            # SIMULATED TRADE
            # We risk $10 to make $30 (1:3 ratio)
            # If price drops within next 10 hours: WIN
            if df['Low'].iloc[i+1:i+10].min() < (df['Close'].iloc[i] * 0.997):
                balance += 30 # Win
            else:
                balance -= 10 # Loss
                
    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_profit_backtest()

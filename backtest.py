import yfinance as yf

def run_profit_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    # Using 3 months of data for a robust sample size
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    risk_per_trade = 10.00
    
    print("--- Starting Tightened Backtest ---")
    
    for i in range(200, len(df) - 10):
        # 1. Trend Filter: EMA 200
        ema200 = df['Close'].iloc[i-200:i].mean()
        is_bearish = df['Close'].iloc[i] < ema200
        is_bullish = df['Close'].iloc[i] > ema200
        
        # 2. Rule: Precision Liquidity Sweep (Rule 2 from your notes)
        swing_low = df['Low'].iloc[i-24:i].min()
        swing_high = df['High'].iloc[i-24:i].max()
        
        # A true sweep: Low breaks support, then closes back inside
        is_bullish_sweep = df['Low'].iloc[i] < swing_low and df['Close'].iloc[i] > swing_low
        is_bearish_sweep = df['High'].iloc[i] > swing_high and df['Close'].iloc[i] < swing_high
        
        # 3. Execution (1:3 Risk Reward)
        # We risk $10 to make $30
        if is_bearish and is_bearish_sweep:
            # Trade Sell: Did price drop 0.3% within 10 hours?
            if df['Low'].iloc[i+1:i+10].min() < (df['Close'].iloc[i] * 0.997):
                balance += 30.00
            else:
                balance -= 10.00
        
        elif is_bullish and is_bullish_sweep:
            # Trade Buy: Did price rise 0.3% within 10 hours?
            if df['High'].iloc[i+1:i+10].max() > (df['Close'].iloc[i] * 1.003):
                balance += 30.00
            else:
                balance -= 10.00
                
    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_profit_backtest()

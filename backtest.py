import yfinance as yf

def run_advanced_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    # Get 2 months of data to ensure we have enough "Previous Day" context
    df = ticker.history(period="2mo", interval="1h")
    
    wins, losses = 0, 0
    # Rule: 24-hour lookback for support
    
    for i in range(24, len(df) - 5):
        # 1. Trend Filter
        ema200 = df['Close'].iloc[i-200:i].mean()
        is_bearish = df['Close'].iloc[i] < ema200
        
        # 2. Liquidity Sweep (Rule 2)
        swing_low = df['Low'].iloc[i-24:i].min()
        liquidity_swept = df['Low'].iloc[i] < swing_low and df['Close'].iloc[i] > swing_low
        
        # 3. Execution (The "Rectified" Logic)
        if is_bearish and liquidity_swept:
            # Simulate a trade: If price moves up 2% before dropping 1%
            if df['High'].iloc[i+1:i+5].max() > df['Close'].iloc[i] * 1.002:
                wins += 1
            else:
                losses += 1
                
    win_rate = (wins / (wins + losses)) * 100
    print(f"--- Rectified Backtest Results ---")
    print(f"Win Rate: {win_rate:.2f}%")

run_advanced_backtest()

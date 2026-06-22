import yfinance as yf

def test_price_action():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1mo", interval="1h")
    
    balance = 1000.00
    sl = 0.0020
    tp = 0.0046
    
    print("--- Backtesting Strategy #3: Price Action (Engulfing) ---")
    
    for i in range(24, len(df) - 10):
        # Identify key level (High/Low of yesterday)
        key_high = df['High'].iloc[i-24:i].max()
        key_low = df['Low'].iloc[i-24:i].min()
        
        # Check for Bearish Engulfing at Key High
        if df['High'].iloc[i] >= key_high:
            if df['Open'].iloc[i] > df['Close'].iloc[i] and df['Close'].iloc[i] < df['Open'].iloc[i-1]:
                # Sell
                if df['Low'].iloc[i+1:i+12].min() < (df['Close'].iloc[i] - tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10
                    
        # Check for Bullish Engulfing at Key Low
        elif df['Low'].iloc[i] <= key_low:
            if df['Open'].iloc[i] < df['Close'].iloc[i] and df['Close'].iloc[i] > df['Open'].iloc[i-1]:
                # Buy
                if df['High'].iloc[i+1:i+12].max() > (df['Close'].iloc[i] + tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10

    print(f"--- Final Balance after Price Action: ${balance:.2f} ---")

test_price_action()

import yfinance as yf

def test_price_action_45pip():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1mo", interval="1h")
    
    balance = 1000.00
    sl = 0.0020  # 20 pips
    tp = 0.0045  # 45 pips (1:2.25 RR)
    
    print("--- Backtesting Price Action (45-pip Target) ---")
    
    for i in range(24, len(df) - 10):
        # Key Levels: Highs/Lows of the last 24 hours
        key_high = df['High'].iloc[i-24:i].max()
        key_low = df['Low'].iloc[i-24:i].min()
        
        # Bearish Engulfing at Key High
        if df['High'].iloc[i] >= key_high:
            if df['Open'].iloc[i] > df['Close'].iloc[i] and df['Close'].iloc[i] < df['Open'].iloc[i-1]:
                # Sell: Target 45 pips
                if df['Low'].iloc[i+1:i+15].min() < (df['Close'].iloc[i] - tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10
                    
        # Bullish Engulfing at Key Low
        elif df['Low'].iloc[i] <= key_low:
            if df['Open'].iloc[i] < df['Close'].iloc[i] and df['Close'].iloc[i] > df['Open'].iloc[i-1]:
                # Buy: Target 45 pips
                if df['High'].iloc[i+1:i+15].max() > (df['Close'].iloc[i] + tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10

    print(f"--- Final Balance after 45-pip Test: ${balance:.2f} ---")

test_price_action_45pip()

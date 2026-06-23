import yfinance as yf

# Your Golden Trio
WATCHLIST = ["USDJPY=X", "EURJPY=X", "AUDJPY=X"]

def scan_market():
    print("--- Scanning Golden Trio for Signals ---")
    for pair in WATCHLIST:
        ticker = yf.Ticker(pair)
        df = ticker.history(period="2d", interval="1h")
        
        # Calculate 24h High/Low
        key_high = df['High'].iloc[-25:-1].max()
        key_low = df['Low'].iloc[-25:-1].min()
        
        # Logic: Bullish/Bearish Engulfing
        if df['Low'].iloc[-1] <= key_low and df['Open'].iloc[-1] < df['Close'].iloc[-1] and df['Close'].iloc[-1] > df['Open'].iloc[-2]:
            print(f"🟢 SIGNAL: Bullish Engulfing on {pair}")
        elif df['High'].iloc[-1] >= key_high and df['Open'].iloc[-1] > df['Close'].iloc[-1] and df['Close'].iloc[-1] < df['Open'].iloc[-2]:
            print(f"🔴 SIGNAL: Bearish Engulfing on {pair}")
        else:
            print(f"No signal for {pair}")

if __name__ == "__main__":
    scan_market()

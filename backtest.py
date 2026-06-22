import yfinance as yf

def test_break_and_retest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1mo", interval="1h")
    
    balance = 1000.00
    sl = 0.0020
    tp = 0.0046
    
    print("--- Backtesting Strategy #1: Break and Retest ---")
    
    for i in range(25, len(df) - 10):
        prev_high = df['High'].iloc[i-24:i].max()
        prev_low = df['Low'].iloc[i-24:i].min()
        
        # Breakout occurred
        if df['Close'].iloc[i] > prev_high:
            # Look for retest in next 5 hours
            if df['Low'].iloc[i+1:i+6].min() <= prev_high:
                # Buy at retest
                if df['High'].iloc[i+1:i+12].max() > (prev_high + tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10
                    
        elif df['Close'].iloc[i] < prev_low:
            # Look for retest in next 5 hours
            if df['High'].iloc[i+1:i+6].max() >= prev_low:
                # Sell at retest
                if df['Low'].iloc[i+1:i+12].min() < (prev_low - tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10

    print(f"--- Final Balance after Break and Retest: ${balance:.2f} ---")

test_break_and_retest()

import yfinance as yf

def test_fibonacci():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1mo", interval="1h")
    
    balance = 1000.00
    sl = 0.0020
    tp = 0.0046
    
    print("--- Backtesting Strategy #5: Fibonacci (61.8%) ---")
    
    for i in range(25, len(df) - 10):
        high = df['High'].iloc[i-24:i].max()
        low = df['Low'].iloc[i-24:i].min()
        fib_618 = low + (high - low) * 0.618
        fib_382 = low + (high - low) * 0.382
        
        # Buy at 61.8% Retracement
        if df['Low'].iloc[i] <= fib_618 and df['Close'].iloc[i] > fib_618:
            if df['High'].iloc[i+1:i+12].max() > (df['Close'].iloc[i] + tp):
                balance += (tp * 10000) * 0.10
            else:
                balance -= (sl * 10000) * 0.10
        
        # Sell at 38.2% Retracement (on a downtrend)
        elif df['High'].iloc[i] >= fib_382 and df['Close'].iloc[i] < fib_382:
            if df['Low'].iloc[i+1:i+12].min() < (df['Close'].iloc[i] - tp):
                balance += (tp * 10000) * 0.10
            else:
                balance -= (sl * 10000) * 0.10

    print(f"--- Final Balance after Fibonacci: ${balance:.2f} ---")

test_fibonacci()

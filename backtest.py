import yfinance as yf

def run_confirmation_strategy():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    sl = 0.0020  # 20 pips
    tp = 0.0046  # 46 pips (1:2.3 RR)
    
    print("--- Testing Trend + Confirmation Logic ---")
    
    for i in range(200, len(df) - 10):
        ema200 = df['Close'].iloc[i-200:i].mean()
        high_prev = df['High'].iloc[i-12:i].max()
        low_prev = df['Low'].iloc[i-12:i].min()
        
        # BUY CONFIRMATION: Price sweeps low, then closes ABOVE the low
        if df['Close'].iloc[i] > ema200:
            if df['Low'].iloc[i] < low_prev and df['Close'].iloc[i] > low_prev:
                # Execution
                if df['High'].iloc[i+1:i+12].max() > (df['Close'].iloc[i] + tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10
        
        # SELL CONFIRMATION: Price sweeps high, then closes BELOW the high
        elif df['Close'].iloc[i] < ema200:
            if df['High'].iloc[i] > high_prev and df['Close'].iloc[i] < high_prev:
                # Execution
                if df['Low'].iloc[i+1:i+12].min() < (df['Close'].iloc[i] - tp):
                    balance += (tp * 10000) * 0.10
                else:
                    balance -= (sl * 10000) * 0.10

    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_confirmation_strategy()

import yfinance as yf

def test_ma_pullback():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1mo", interval="1h")
    
    balance = 1000.00
    sl = 0.0020
    tp = 0.0046
    
    print("--- Backtesting Strategy #2: MA Pullback (1 Month) ---")
    
    for i in range(200, len(df) - 10):
        ema200 = df['Close'].iloc[i-200:i].mean()
        
        # Buy: Price is above EMA and pulls back to it
        if df['Close'].iloc[i] > ema200 and df['Low'].iloc[i] <= ema200:
            if df['High'].iloc[i+1:i+12].max() > (df['Close'].iloc[i] + tp):
                balance += (tp * 10000) * 0.10
            else:
                balance -= (sl * 10000) * 0.10
        
        # Sell: Price is below EMA and pulls back to it
        elif df['Close'].iloc[i] < ema200 and df['High'].iloc[i] >= ema200:
            if df['Low'].iloc[i+1:i+12].min() < (df['Close'].iloc[i] - tp):
                balance += (tp * 10000) * 0.10
            else:
                balance -= (sl * 10000) * 0.10
                
    print(f"--- Final Balance after MA Pullback: ${balance:.2f} ---")

test_ma_pullback()

import yfinance as yf

def run_20_45_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    # TP 45 pips = 0.0045, SL 20 pips = 0.0020
    tp_val = 0.0045
    sl_val = 0.0020
    
    print("--- Testing 20 SL / 45 TP Strategy ---")
    
    for i in range(200, len(df) - 10):
        ema200 = df['Close'].iloc[i-200:i].mean()
        fvg_low = float(df['Low'].iloc[i-3])
        fvg_high = float(df['High'].iloc[i-2])
        is_fvg = fvg_low > fvg_high
        
        entry_price = df['Close'].iloc[i]
        
        if df['Close'].iloc[i] < ema200 and is_fvg:
            # Sell Trade
            # Check if price hits TP (entry - 0.0045) before SL (entry + 0.0020)
            if (entry_price - df['Low'].iloc[i+1:i+24].min()) >= tp_val:
                balance += 45
            else:
                balance -= 20
        
        elif df['Close'].iloc[i] > ema200 and is_fvg:
            # Buy Trade
            # Check if price hits TP (entry + 0.0045) before SL (entry - 0.0020)
            if (df['High'].iloc[i+1:i+24].max() - entry_price) >= tp_val:
                balance += 45
            else:
                balance -= 20
                
    print(f"--- Final Account Balance: ${balance:.2f} ---")

run_20_45_backtest()

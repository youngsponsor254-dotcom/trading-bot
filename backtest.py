import yfinance as yf

def run_60_tp_backtest():
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="3mo", interval="1h")
    
    balance = 1000.00
    # TP 60 pips = 0.0060, SL 20 pips = 0.0020
    tp_val = 0.0060
    sl_val = 0.0020
    
    print("--- Testing 20 SL / 60 TP Strategy ---")
    
    for i in range(200, len(df) - 10):
        ema200 = df['Close'].iloc[i-200:i].mean()
        fvg_low = float(df['Low'].iloc[i-3])
        fvg_high = float(df['High'].iloc[i-2])
        is_fvg = fvg_low > fvg_high
        
        entry_price = df['Close'].iloc[i]
        
        if df['Close'].iloc[i] < ema200 and is_fvg:
            # Sell Trade
            if (entry_price - df['Low'].iloc[i+1:i+36].min()) >= tp_val:
                balance += 60
            else:
                balance -= 20
        
        elif df['Close'].iloc[i] > ema200 and is_fvg:
            # Buy Trade
            if (df['High'].iloc[i+1:i+36].max() - entry_price) >= tp_val:
                balance += 60
            else:
                balance -= 20
                
    print(f"--- Final Account Balance with 60 TP: ${balance:.2f} ---")

run_60_tp_backtest()

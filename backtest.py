import yfinance as yf

# Your expanded Yen-centric basket
pairs = ["USDJPY=X", "EURJPY=X", "AUDJPY=X", "CADJPY=X"]

def backtest_yen_basket_v2():
    total_balance = 1000.00
    # Risk is now split across 4 pairs
    risk_per_trade = (total_balance * 0.02) / 4 
    
    print(f"--- Backtesting 4-Pair Yen Basket ---")
    
    for pair in pairs:
        ticker = yf.Ticker(pair)
        df = ticker.history(period="1mo", interval="1h")
        
        pair_balance = 0 
        
        for i in range(24, len(df) - 10):
            key_high = df['High'].iloc[i-24:i].max()
            key_low = df['Low'].iloc[i-24:i].min()
            
            # Bearish Engulfing
            if df['High'].iloc[i] >= key_high:
                if df['Open'].iloc[i] > df['Close'].iloc[i] and df['Close'].iloc[i] < df['Open'].iloc[i-1]:
                    # Sell
                    if df['Low'].iloc[i+1:i+15].min() < (df['Close'].iloc[i] - 0.0045):
                        pair_balance += (risk_per_trade * 2.25)
                    else:
                        pair_balance -= risk_per_trade
            
            # Bullish Engulfing
            elif df['Low'].iloc[i] <= key_low:
                if df['Open'].iloc[i] < df['Close'].iloc[i] and df['Close'].iloc[i] > df['Open'].iloc[i-1]:
                    # Buy
                    if df['High'].iloc[i+1:i+15].max() > (df['Close'].iloc[i] + 0.0045):
                        pair_balance += (risk_per_trade * 2.25)
                    else:
                        pair_balance -= risk_per_trade
                        
        print(f"{pair} Result: ${pair_balance:.2f}")
        total_balance += pair_balance
        
    print(f"--- Final Combined Balance: ${total_balance:.2f} ---")

backtest_yen_basket_v2()

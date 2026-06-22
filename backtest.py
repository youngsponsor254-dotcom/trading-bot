import yfinance as yf
import pandas as pd

def run_backtest():
    print("Starting Backtest...")
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1y", interval="1h")
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    wins = 0
    losses = 0
    
    # Iterate through candles (skipping first 200 for EMA warm-up)
    for i in range(200, len(df) - 5):
        # Setup logic: Candle i-2 and i-1
        c1_high = df['High'].iloc[i-2]
        c3_low = df['Low'].iloc[i-1]
        
        # Bullish FVG check
        if c3_low > c1_high and df['Close'].iloc[i] > df['EMA200'].iloc[i]:
            # Simple simulation: Did price go up in the next 5 hours?
            if df['Close'].iloc[i+5] > df['Close'].iloc[i]:
                wins += 1
            else:
                losses += 1
                
    print(f"--- Results ---")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    if (wins + losses) > 0:
        win_rate = (wins / (wins + losses)) * 100
        print(f"Win Rate: {win_rate:.2f}%")

run_backtest()

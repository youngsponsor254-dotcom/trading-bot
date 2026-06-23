import yfinance as yf
from discord import SyncWebhook
import time

# --- CONFIGURATION ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
webhook = SyncWebhook.from_url(WEBHOOK_URL)
WATCHLIST = ["USDJPY=X", "EURJPY=X", "AUDJPY=X"]
active_trades = []

print("--- Bot Started: 15-Minute Mode (Heartbeat 1h) ---")

# Counter to track hours for heartbeat (4 cycles of 15m = 1 hour)
heartbeat_counter = 0

while True:
    # --- 1-Hour Heartbeat Logic ---
    if heartbeat_counter >= 4:
        webhook.send("🤖 Hourly Check: Bot is active and scanning...")
        heartbeat_counter = 0
    heartbeat_counter += 1
    
    # --- SCANNING LOOP ---
    for pair in WATCHLIST:
        ticker = yf.Ticker(pair)
        df = ticker.history(period="2d", interval="15m")
        
        # 24h High/Low (96 candles = 24 hours)
        key_high = df['High'].iloc[-97:-1].max()
        key_low = df['Low'].iloc[-97:-1].min()
        
        # Determine Signal
        signal_message = None
        
        # Bullish
        if df['Low'].iloc[-1] <= key_low and df['Open'].iloc[-1] < df['Close'].iloc[-1] and df['Close'].iloc[-1] > df['Open'].iloc[-2]:
            sl = df['Low'].iloc[-1] - 0.0020
            tp = df['Close'].iloc[-1] + 0.0040
            signal_message = f"🟢 **BUY SIGNAL: {pair}**\nEntry: {df['Close'].iloc[-1]:.4f}\nSL: {sl:.4f}\nTP: {tp:.4f}"
            
        # Bearish
        elif df['High'].iloc[-1] >= key_high and df['Open'].iloc[-1] > df['Close'].iloc[-1] and df['Close'].iloc[-1] < df['Open'].iloc[-2]:
            sl = df['High'].iloc[-1] + 0.0020
            tp = df['Close'].iloc[-1] - 0.0040
            signal_message = f"🔴 **SELL SIGNAL: {pair}**\nEntry: {df['Close'].iloc[-1]:.4f}\nSL: {sl:.4f}\nTP: {tp:.4f}"
            
        # Send double alert if signal found
        if signal_message:
            webhook.send(signal_message)
            time.sleep(30) # 30s interval
            webhook.send(signal_message)

    # --- TP/SL CHECK ---
    for trade in active_trades[:]:
        # Simple update check...
        pass # Add your custom tracking logic here if needed
            
    # Wait for the remainder of the 15-minute cycle
    time.sleep(870)

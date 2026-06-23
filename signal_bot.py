import yfinance as yf
from discord import SyncWebhook
import time

# --- CONFIGURATION ---
# Replace the URL below with your actual Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
webhook = SyncWebhook.from_url(WEBHOOK_URL)
WATCHLIST = ["USDJPY=X", "EURJPY=X", "AUDJPY=X"]

print("--- Bot Started: 15-Minute Scanning Mode ---")

# --- MAIN LOOP ---
while True:
    # Send a heartbeat message to confirm the bot is active
    webhook.send("🤖 Bot is active and scanning the market...")
    
    for pair in WATCHLIST:
        ticker = yf.Ticker(pair)
        # Fetch 15-minute interval data
        df = ticker.history(period="2d", interval="15m")
        
        # Calculate 24h High/Low (last 96 candles = 24 hours)
        key_high = df['High'].iloc[-97:-1].max()
        key_low = df['Low'].iloc[-97:-1].min()
        
        # Bullish Engulfing Logic
        if df['Low'].iloc[-1] <= key_low and df['Open'].iloc[-1] < df['Close'].iloc[-1] and df['Close'].iloc[-1] > df['Open'].iloc[-2]:
            webhook.send(f"🟢 BULLISH (15m): {pair} at {key_low:.4f}")
            
        # Bearish Engulfing Logic
        elif df['High'].iloc[-1] >= key_high and df['Open'].iloc[-1] > df['Close'].iloc[-1] and df['Close'].iloc[-1] < df['Open'].iloc[-2]:
            webhook.send(f"🔴 BEARISH (15m): {pair} at {key_high:.4f}")
            
    # Wait 15 minutes (900 seconds) before the next scan
    time.sleep(900)

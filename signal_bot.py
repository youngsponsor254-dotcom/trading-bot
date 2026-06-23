import yfinance as yf
from discord import SyncWebhook
import time

# Paste your Webhook URL here
WEBHOOK_URL = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
webhook = SyncWebhook.from_url(WEBHOOK_URL)
WATCHLIST = ["USDJPY=X", "EURJPY=X", "AUDJPY=X"]

print("--- Bot Started: 15-Minute Scanning Mode ---")

while True:
    for pair in WATCHLIST:
        ticker = yf.Ticker(pair)
        # CHANGED: interval is now 15m
        df = ticker.history(period="2d", interval="15m")
        
        # 24h High/Low (adjusted for 15m intervals, taking last 96 candles)
        key_high = df['High'].iloc[-97:-1].max()
        key_low = df['Low'].iloc[-97:-1].min()
        
        # Bullish Logic
        if df['Low'].iloc[-1] <= key_low and df['Open'].iloc[-1] < df['Close'].iloc[-1] and df['Close'].iloc[-1] > df['Open'].iloc[-2]:
            webhook.send(f"🟢 BULLISH (15m): {pair} at {key_low:.4f}")
        # Bearish Logic
        elif df['High'].iloc[-1] >= key_high and df['Open'].iloc[-1] > df['Close'].iloc[-1] and df['Close'].iloc[-1] < df['Open'].iloc[-2]:
            webhook.send(f"🔴 BEARISH (15m): {pair} at {key_high:.4f}")
            
    # CHANGED: 900 seconds = 15 minutes
    time.sleep(900)

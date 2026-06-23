import yfinance as yf
from discord import SyncWebhook
import time
from datetime import datetime

# --- CONFIGURATION ---
# IMPORTANT: Put your actual Webhook URL inside the quotes below!
WEBHOOK_URL = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
webhook = SyncWebhook.from_url(WEBHOOK_URL)

WATCHLIST = {
    "USDJPY=X": 0.15,
    "EURJPY=X": 0.15,
    "AUDJPY=X": 0.18
}

def log_signal(message):
    with open("signals.txt", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

print("--- Fresh Bot Started ---")
webhook.send("🚀 Bot successfully restarted and is now watching the markets.")

while True:
    try:
        for pair, lot_size in WATCHLIST.items():
            ticker = yf.Ticker(pair)
            df = ticker.history(period="2d", interval="15m")
            
            if len(df) < 97: continue
            
            key_high = df['High'].iloc[-97:-1].max()
            key_low = df['Low'].iloc[-97:-1].min()
            
            # Simplified Logic
            if df['Low'].iloc[-1] <= key_low and df['Open'].iloc[-1] < df['Close'].iloc[-1]:
                msg = f"🟢 BUY {pair} (Lot: {lot_size}) @ {df['Close'].iloc[-1]:.3f}"
                webhook.send(msg)
                log_signal(msg)
            elif df['High'].iloc[-1] >= key_high and df['Open'].iloc[-1] > df['Close'].iloc[-1]:
                msg = f"🔴 SELL {pair} (Lot: {lot_size}) @ {df['Close'].iloc[-1]:.3f}"
                webhook.send(msg)
                log_signal(msg)

    except Exception as e:
        print(f"Error: {e}")
    time.sleep(300)

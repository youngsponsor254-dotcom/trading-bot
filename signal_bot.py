import yfinance as yf
from discord import SyncWebhook
import time
from datetime import datetime
import os

# --- CONFIGURATION ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
webhook = SyncWebhook.from_url(WEBHOOK_URL)
LOG_FILE = "signals.txt"

WATCHLIST = {
    "USDJPY=X": 0.15,
    "EURJPY=X": 0.15,
    "AUDJPY=X": 0.18
}

def log_signal(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def send_startup_summary():
    """Reads the log file and sends past signals to Discord."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            if lines:
                webhook.send("🔔 **Bot restarted! Here are the signals from while I was away:**")
                # Send the last 5 signals to avoid spamming Discord
                for line in lines[-5:]: 
                    webhook.send(line.strip())
            else:
                webhook.send("🤖 Bot started. No previous signals found.")
    else:
        webhook.send("🤖 Bot started. Log file created.")

# --- STARTUP ---
print("--- Bot Initializing ---")
send_startup_summary()

while True:
    try:
        for pair, lot_size in WATCHLIST.items():
            ticker = yf.Ticker(pair)
            df = ticker.history(period="2d", interval="15m")
            if len(df) < 97: continue
            
            key_high = df['High'].iloc[-97:-1].max()
            key_low = df['Low'].iloc[-97:-1].min()
            
            # Simplified Logic for demonstration
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

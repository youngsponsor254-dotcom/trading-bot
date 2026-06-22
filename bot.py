import requests
import yfinance as yf
import time
from datetime import datetime

# --- CONFIGURATION ---
# PASTE YOUR REAL DISCORD WEBHOOK URL BELOW
WEBHOOK_URL = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    """Sends a message to Discord with basic error handling."""
    try:
        response = requests.post(WEBHOOK_URL, json={"content": message}, timeout=10)
        if response.status_code != 204:
            print(f"DEBUG: Discord API returned code {response.status_code}")
    except Exception as e:
        print(f"DEBUG: Discord Error: {e}")

# --- MAIN LOGIC ---
try:
    ticker = yf.Ticker("GBPUSD=X")
    # Fetch 20 days of data for reliable EMA calculation
    df = ticker.history(period="20d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    
    current_hour = datetime.now().hour # UTC Time
    
    if len(df) >= 3:
        # FVG logic: Compare Candle 1 (i-3) and Candle 3 (i-2)
        fvg_low = float(df['Low'].iloc[-3])
        fvg_high = float(df['High'].iloc[-2])
        
        is_bullish_fvg = fvg_low > fvg_high
        is_bearish_fvg = fvg_high < fvg_low
        
        # Check if price has entered the gap (Consumed)
        is_filled = latest_price >= fvg_high and latest_price <= fvg_low
        
        # Determine signals
        if is_bullish_fvg and not is_filled and latest_price > ema200:
            msg = "@here 🚀 **POSSIBLE BUY: BULLISH FVG DETECTED.** Price: `{latest_price:.5f}`"
            for _ in range(3): send_discord_alert(msg); time.sleep(2)
            
        elif is_bearish_fvg and not is_filled and latest_price < ema200:
            msg = "@here 📉 **POSSIBLE SELL: BEARISH FVG DETECTED.** Price: `{latest_price:.5f}`"
            for _ in range(3): send_discord_alert(msg); time.sleep(2)
            
        elif is_bullish_fvg and is_filled:
            print("FVG detected but currently filled (consumed). Staying quiet.")
            
        # Daily Heartbeat at 08:00 UTC
        elif current_hour == 8:
            send_discord_alert(f"🕒 **HEARTBEAT:** Bot Online. Price: `{latest_price:.5f}` | EMA200: `{ema200:.5f}`")
        else:
            print(f"Market quiet. Price: {latest_price:.5f} | EMA: {ema200:.5f}")
    else:
        print("Waiting for more market data...")

except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

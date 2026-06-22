import requests
import yfinance as yf
import time
from datetime import datetime

webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    try:
        requests.post(webhook_url, json={"content": message}, timeout=10)
    except Exception as e:
        print(f"Discord error: {e}")

try:
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="20d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    
    current_hour = datetime.now().hour
    
    if len(df) >= 3:
        # FVG Boundaries
        fvg_low = float(df['Low'].iloc[-3])
        fvg_high = float(df['High'].iloc[-2])
        
        # Bullish: Gap Up | Bearish: Gap Down
        is_bullish_fvg = fvg_low > fvg_high # Logic for Bullish gap
        is_bearish_fvg = fvg_high < fvg_low # Logic for Bearish gap
        
        is_filled = latest_price >= fvg_high and latest_price <= fvg_low
        
        # Alerts
        if is_bullish_fvg and not is_filled and latest_price > ema200:
            msg = "@here 🚀 **POSSIBLE BUY: BULLISH FVG DETECTED.** Price: `{latest_price:.5f}`."
            for i in range(3): send_discord_alert(msg); time.sleep(2)
            
        elif is_bearish_fvg and not is_filled and latest_price < ema200:
            msg = "@here 📉 **POSSIBLE SELL: BEARISH FVG DETECTED.** Price: `{latest_price:.5f}`."
            for i in range(3): send_discord_alert(msg); time.sleep(2)
            
        elif current_hour == 8:
            send_discord_alert(f"🕒 **HEARTBEAT:** Price: `{latest_price:.5f}` | EMA200: `{ema200:.5f}`.")
            
    else:
        print("Market data loading...")
except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

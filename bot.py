import requests
import yfinance as yf
import time
from datetime import datetime

webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    print(f"DEBUG: Attempting to send: {message}")
    try:
        response = requests.post(webhook_url, json={"content": message}, timeout=10)
        print(f"DEBUG: Discord Status Code: {response.status_code}")
    except Exception as e:
        print(f"DEBUG: Discord Error: {e}")

print("DEBUG: Bot starting...")
try:
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="20d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    
    current_hour = datetime.now().hour
    print(f"DEBUG: Price: {latest_price}, EMA: {ema200}, Hour: {current_hour}")

    if len(df) >= 3:
        fvg_low = float(df['Low'].iloc[-3])
        fvg_high = float(df['High'].iloc[-2])
        is_bullish_fvg = fvg_low > fvg_high
        is_bearish_fvg = fvg_high < fvg_low
        is_filled = latest_price >= fvg_high and latest_price <= fvg_low
        
        print(f"DEBUG: Bullish: {is_bullish_fvg}, Bearish: {is_bearish_fvg}, Filled: {is_filled}")

        if is_bullish_fvg and not is_filled and latest_price > ema200:
            msg = "@here 🚀 **POSSIBLE BUY: BULLISH FVG DETECTED.**"
            for i in range(3): send_discord_alert(msg); time.sleep(2)
        elif is_bearish_fvg and not is_filled and latest_price < ema200:
            msg = "@here 📉 **POSSIBLE SELL: BEARISH FVG DETECTED.**"
            for i in range(3): send_discord_alert(msg); time.sleep(2)
        send_discord_alert(f"🕒 **TEST HEARTBEAT:** The bot is alive! Price: {latest_price:.5f}")
        else:
            print("DEBUG: No conditions met. Quiet mode.")
    else:
        print("DEBUG: Not enough data.")
except Exception as e:
    print(f"DEBUG: CRITICAL ERROR: {e}")

import requests
import yfinance as yf
import time
from datetime import datetime

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message}, timeout=10)
    except Exception as e:
        print(f"DEBUG: Discord Error: {e}")

try:
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="20d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    current_hour = datetime.now().hour
    
    if len(df) >= 4:
        # FVG Boundaries
        fvg_low = float(df['Low'].iloc[-3])
        fvg_high = float(df['High'].iloc[-2])
        is_bullish_fvg = fvg_low > fvg_high
        is_bearish_fvg = fvg_high < fvg_low
        is_filled = latest_price >= fvg_high and latest_price <= fvg_low
        
        # Liquidity Filter Logic
        # Buy: Price swept a previous low
        prev_low = float(df['Low'].iloc[-4])
        has_swept_low = float(df['Low'].iloc[-3]) < prev_low
        
        # Sell: Price swept a previous high
        prev_high = float(df['High'].iloc[-4])
        has_swept_high = float(df['High'].iloc[-3]) > prev_high
        
        # High Probability Signal Checks
        if is_bullish_fvg and not is_filled and latest_price > ema200 and has_swept_low:
            msg = "@here 🚀 **LIQUIDITY SWEEP + BULLISH FVG!** Price: `{latest_price:.5f}`"
            for _ in range(3): send_discord_alert(msg); time.sleep(2)
            
        elif is_bearish_fvg and not is_filled and latest_price < ema200 and has_swept_high:
            msg = "@here 📉 **LIQUIDITY SWEEP + BEARISH FVG!** Price: `{latest_price:.5f}`"
            for _ in range(3): send_discord_alert(msg); time.sleep(2)
            
        elif current_hour == 8:
            send_discord_alert(f"🕒 **HEARTBEAT:** Bot Active. Price: `{latest_price:.5f}`")
        else:
            print(f"Market conditions quiet. Price: {latest_price:.5f}")
    else:
        print("Waiting for more market data...")

except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

import requests
import yfinance as yf

# PASTE YOUR REAL DISCORD WEBHOOK URL BELOW
webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    print(f"Sending to Discord: {message}")
    if "YOUR_ACTUAL_ID_HERE" not in webhook_url:
        try:
            requests.post(webhook_url, json={"content": message}, timeout=10)
        except Exception as e:
            print(f"Discord error: {e}")

try:
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    
    # Logic: Always send an update, even if no FVG is found
    if len(df) >= 3:
        candle1_high = float(df['High'].iloc[-3])
        candle3_low = float(df['Low'].iloc[-2])
        
        if candle3_low > candle1_high:
            msg = f"📈 **BULLISH FVG DETECTED!**\nPrice `{latest_price:.5f}` is near the gap (`{candle1_high:.5f} - {candle3_low:.5f}`)."
        else:
            msg = f"🕒 **MARKET UPDATE:**\nPrice is `{latest_price:.5f}`. No FVG currently detected. Still monitoring..."
    else:
        msg = f"🕒 **MARKET UPDATE:**\nPrice is `{latest_price:.5f}`. Data is still loading..."
    
    send_discord_alert(msg)
except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

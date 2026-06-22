import requests
import yfinance as yf

# PASTE YOUR FULL WEBHOOK URL HERE
webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    try:
        requests.post(webhook_url, json={"content": message}, timeout=10)
    except Exception as e:
        print(f"Discord error: {e}")

try:
    ticker = yf.Ticker("GBPUSD=X")
    # Changed to 5d to ensure we have plenty of data to work with
    df = ticker.history(period="5d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    
    if len(df) >= 3:
        candle1_high = float(df['High'].iloc[-3])
        candle3_low = float(df['Low'].iloc[-2])
        
        if candle3_low > candle1_high:
            msg = f"📈 **BULLISH FVG DETECTED!**\nPrice `{latest_price:.5f}` is near the gap."
        else:
            msg = f"🕒 **MARKET UPDATE:** Price is `{latest_price:.5f}`. No FVG gap detected right now."
    else:
        msg = "⚠️ Market data is still loading or insufficient."
        
    send_discord_alert(msg)
except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

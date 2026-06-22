import requests
import yfinance as yf

# PASTE YOUR REAL DISCORD WEBHOOK URL BELOW
# Example: "https://discord.com/api/webhooks/123456789/..."
webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    print(f"Sending to Discord: {message}")
    if "PASTE_YOUR_REAL" not in webhook_url:
        try:
            payload = {"content": message}
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 204:
                print("Message sent successfully!")
            else:
                print(f"Discord returned status code: {response.status_code}")
        except Exception as e:
            print(f"Discord connection error: {e}")
    else:
        print("Webhook URL not configured!")

print("Fetching latest GBP/USD market structure...")
try:
    # 1. Fetch data using '1d' to ensure yfinance has enough buffer
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    
    # 2. Logic: Always report something so you know the bot is alive
    if len(df) >= 3:
        # Get candles for FVG calculation
        candle1_high = float(df['High'].iloc[-3])
        candle3_low = float(df['Low'].iloc[-2])
        
        if candle3_low > candle1_high:
            msg = f"📈 **BULLISH FVG DETECTED!**\nPrice `{latest_price:.5f}` is near the gap (`{candle1_high:.5f} - {candle3_low:.5f}`)."
        else:
            msg = f"🕒 **MARKET STATUS:**\nPrice: `{latest_price:.5f}`. No FVG currently detected. Still monitoring..."
    else:
        msg = f"🕒 **MARKET STATUS:**\nPrice: `{latest_price:.5f}`. Initializing market data..."
    
    send_discord_alert(msg)
except Exception as e:
    print(f"Analysis failed: {e}")
    send_discord_alert(f"❌ Bot error: {e}")

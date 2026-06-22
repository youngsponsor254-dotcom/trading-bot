import requests
import yfinance as yf

# PASTE YOUR REAL DISCORD WEBHOOK URL BELOW
# It should look like: "https://discord.com/api/webhooks/..."
webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    print(f"Sending to Discord: {message}")
    if "YOUR_ACTUAL_WEBHOOK_URL_HERE" not in webhook_url:
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
    # 1. Fetch data using '1d' which is required by yfinance
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="1d", interval="1h")
    
    # 2. Check if we have enough data
    if len(df) >= 3:
        # Get the High of 3 hours ago and Low of 2 hours ago
        candle1_high = float(df['High'].iloc[-3])
        candle3_low = float(df['Low'].iloc[-2])
        latest_price = float(ticker.fast_info['last_price'])
        
        # 3. Check for Bullish FVG
        if candle3_low > candle1_high:
            fvg_bottom = candle1_high
            fvg_top = candle3_low
            
            if fvg_bottom <= latest_price <= fvg_top:
                msg = f"📈 **BULLISH FVG DETECTED!**\nPrice `{latest_price:.5f}` is inside the zone (`{fvg_bottom:.5f} - {fvg_top:.5f}`)."
            else:
                msg = f"🕒 **MARKET STATUS:**\nPrice `{latest_price:.5f}`. Outside your FVG zone (`{fvg_bottom:.5f} - {fvg_top:.5f}`)."
            
            send_discord_alert(msg)
        else:
            send_discord_alert("🔍 No FVG detected in current market structure.")
    else:
        send_discord_alert("⚠️ Insufficient market data yet.")
except Exception as e:
    print(f"Analysis failed: {e}")
    send_discord_alert(f"❌ Bot error: {e}")

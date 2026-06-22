import requests
import yfinance as yf

# Replace this with your actual Discord Webhook URL
webhook_url = "PASTE_YOUR_REAL_DISCORD_WEBHOOK_URL_HERE"

def send_discord_alert(message):
    print(message)
    if "PASTE_YOUR_REAL" not in webhook_url:
        try:
            requests.post(webhook_url, json={"content": message}, timeout=10)
        except Exception as e:
            print(f"Discord error: {e}")

print("Fetching latest GBP/USD market structure...")
try:
    ticker = yf.Ticker("GBPUSD=X")
    df = ticker.history(period="5h", interval="1h")
    
    if len(df) >= 3:
        candle1_high = float(df['High'].iloc[-3])
        candle3_low = float(df['Low'].iloc[-2])
        latest_price = float(ticker.fast_info['last_price'])
        
        if candle3_low > candle1_high:
            fvg_bottom = candle1_high
            fvg_top = candle3_low
            
            if fvg_bottom <= latest_price <= fvg_top:
                msg = f"📈 **BULLISH FVG DETECTED!**\nPrice `{latest_price:.5f}` is in the zone (`{fvg_bottom:.5f} - {fvg_top:.5f}`)."
                send_discord_alert(msg)
            else:
                print(f"Price {latest_price:.5f} is outside the zone.")
        else:
            print("No new FVG detected.")
    else:
        print("Not enough market data.")
except Exception as e:
    print(f"Analysis failed: {e}")

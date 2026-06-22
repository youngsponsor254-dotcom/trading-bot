import requests
import yfinance as yf

# PASTE YOUR WEBHOOK URL HERE
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
    
    if len(df) >= 3:
        # Define the Gap boundaries
        fvg_bottom = float(df['High'].iloc[-3])
        fvg_top = float(df['Low'].iloc[-2])
        
        is_bullish_fvg = fvg_top > fvg_bottom
        is_filled = latest_price >= fvg_bottom and latest_price <= fvg_top
        trend_up = latest_price > ema200
        
        if is_bullish_fvg:
            if is_filled:
                msg = f"📉 **FVG CONSUMED:** Price `{latest_price:.5f}` has filled the FVG. Discarding zone."
            elif trend_up:
                msg = f"🚀 **HIGH PROBABILITY BULLISH FVG!** Zone: `{fvg_bottom:.5f} - {fvg_top:.5f}`."
            else:
                msg = f"⚠️ **BULLISH FVG DETECTED** but Price is BELOW 200 EMA. Skipping trade."
        else:
            msg = f"🕒 **MARKET STATUS:** Price `{latest_price:.5f}` | EMA200: `{ema200:.5f}`. No active FVG."
    else:
        msg = "⚠️ Collecting more market data..."
        
    send_discord_alert(msg)
except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

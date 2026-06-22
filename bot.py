import requests
import yfinance as yf

webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    try:
        requests.post(webhook_url, json={"content": message}, timeout=10)
    except Exception as e:
        print(f"Discord error: {e}")

try:
    ticker = yf.Ticker("GBPUSD=X")
    # Fetch 20 days of hourly data to ensure we have enough for a 200-period EMA
    df = ticker.history(period="20d", interval="1h")
    latest_price = float(ticker.fast_info['last_price'])
    
    # Calculate 200-period EMA
    ema200 = df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
    
    # Logic: Only alert Bullish if price is ABOVE EMA200 (Trend Filter)
    if len(df) >= 200:
        candle1_high = float(df['High'].iloc[-3])
        candle3_low = float(df['Low'].iloc[-2])
        
        is_bullish_fvg = candle3_low > candle1_high
        trend_is_up = latest_price > ema200
        
        if is_bullish_fvg and trend_is_up:
            msg = f"🚀 **HIGH PROBABILITY BULLISH FVG!**\nPrice `{latest_price:.5f}` is above 200 EMA (`{ema200:.5f}`)."
        elif is_bullish_fvg:
            msg = f"⚠️ **BULLISH FVG DETECTED** but Price `{latest_price:.5f}` is BELOW 200 EMA. Skipping trade."
        else:
            msg = f"🕒 **MARKET STATUS:** Price `{latest_price:.5f}` | 200 EMA: `{ema200:.5f}`. No FVG."
    else:
        msg = "⚠️ Collecting more market data for EMA calculation..."
        
    send_discord_alert(msg)
except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

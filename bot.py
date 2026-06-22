import requests
import yfinance as yf
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
    
    if len(df) >= 4:
        fvg_low = float(df['Low'].iloc[-3])
        fvg_high = float(df['High'].iloc[-2])
        is_bullish_fvg = fvg_low > fvg_high
        is_bearish_fvg = fvg_high < fvg_low
        is_filled = latest_price >= fvg_high and latest_price <= fvg_low
        
        # Liquidity Logic
        prev_low = float(df['Low'].iloc[-4])
        has_swept_low = float(df['Low'].iloc[-3]) < prev_low
        
        # --- THE FULL REPORT LOGIC ---
        report = f"📊 **MARKET REPORT**\n"
        report += f"Price: `{latest_price:.5f}` | EMA200: `{ema200:.5f}`\n"
        report += f"Bullish FVG: `{is_bullish_fvg}` | Swept Low: `{has_swept_low}`\n"
        
        if is_bullish_fvg and not is_filled and latest_price > ema200 and has_swept_low:
            report += "🚀 **SIGNAL: POSSIBLE BUY!**"
        elif is_bearish_fvg and not is_filled and latest_price < ema200:
            report += "📉 **SIGNAL: POSSIBLE SELL!**"
        else:
            report += "Status: No high-prob setup found."

        send_discord_alert(report)
        print(report)
    else:
        send_discord_alert("⚠️ Collecting data...")

except Exception as e:
    send_discord_alert(f"❌ Error: {e}")

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
    support_level = float(df['Low'].tail(24).min())
    
    if len(df) >= 4:
        # FVG logic
        fvg_low = float(df['Low'].iloc[-3])
        fvg_high = float(df['High'].iloc[-2])
        is_bullish_fvg = fvg_low > fvg_high
        is_bearish_fvg = fvg_high < fvg_low
        is_filled = latest_price >= fvg_high and latest_price <= fvg_low
        
        # Liquidity Filter
        has_swept_low = float(df['Low'].iloc[-3]) < float(df['Low'].iloc[-4])
        has_swept_high = float(df['High'].iloc[-3]) > float(df['High'].iloc[-4])
        
        # Analysis Report
        report = f"📊 **MARKET REPORT**\nPrice: `{latest_price:.5f}` | EMA200: `{ema200:.5f}`\n"
        
        # Dual-Bias Logic
        if latest_price < ema200:
            report += "Bias: **BEARISH** (Selling Preference)\n"
            if is_bearish_fvg and not is_filled and has_swept_high:
                report += "📉 **SIGNAL: HIGH-PROB SELL (TREND)**"
            elif is_bullish_fvg and latest_price <= (support_level * 1.002):
                report += "⚠️ **SIGNAL: COUNTER-TREND BUY (AT SUPPORT)**"
            else:
                report += "Status: Waiting for Sell setup..."
        else:
            report += "Bias: **BULLISH** (Buying Preference)\n"
            if is_bullish_fvg and not is_filled and has_swept_low:
                report += "🚀 **SIGNAL: HIGH-PROB BUY (TREND)**"
            else:
                report += "Status: Waiting for Buy setup..."
        
        send_discord_alert(report)
        print(report)
    else:
        send_discord_alert("⚠️ Collecting data...")

except Exception as e:
    send_discord_alert(f"❌ Bot Error: {e}")

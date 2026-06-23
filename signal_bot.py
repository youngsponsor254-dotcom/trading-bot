import yfinance as yf
import discord
import asyncio

# --- YOUR CONFIG ---
TOKEN = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
CHANNEL_ID = 123456789012345678  # Replace with your actual Channel ID
WATCHLIST = ["USDJPY=X", "EURJPY=X", "AUDJPY=X"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_market():
    channel = client.get_channel(CHANNEL_ID)
    print("Scanning market...")
    for pair in WATCHLIST:
        ticker = yf.Ticker(pair)
        df = ticker.history(period="2d", interval="1h")
        
        # Logic: 24h levels + Engulfing
        key_high = df['High'].iloc[-25:-1].max()
        key_low = df['Low'].iloc[-25:-1].min()
        
        # Bullish
        if df['Low'].iloc[-1] <= key_low and df['Open'].iloc[-1] < df['Close'].iloc[-1] and df['Close'].iloc[-1] > df['Open'].iloc[-2]:
            await channel.send(f"🟢 BULLISH ENGULFING: {pair}")
        # Bearish
        elif df['High'].iloc[-1] >= key_high and df['Open'].iloc[-1] > df['Close'].iloc[-1] and df['Close'].iloc[-1] < df['Open'].iloc[-2]:
            await channel.send(f"🔴 BEARISH ENGULFING: {pair}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    while True:
        await check_market()
        await asyncio.sleep(3600) # Scans every 1 hour

client.run(TOKEN)

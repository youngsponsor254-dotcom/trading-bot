import yfinance as yf
import discord
from discord.ext import tasks

# Replace these with your actual details
TOKEN = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
CHANNEL_ID = 123456789012345678 
WATCHLIST = ["USDJPY=X", "EURJPY=X", "AUDJPY=X"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(minutes=30)
async def scan_market():
    channel = client.get_channel(CHANNEL_ID)
    if not channel: return
    
    for pair in WATCHLIST:
        ticker = yf.Ticker(pair)
        df = ticker.history(period="2d", interval="1h")
        key_high = df['High'].iloc[-25:-1].max()
        key_low = df['Low'].iloc[-25:-1].min()
        
        # Bullish Engulfing
        if df['Low'].iloc[-1] <= key_low and df['Open'].iloc[-1] < df['Close'].iloc[-1] and df['Close'].iloc[-1] > df['Open'].iloc[-2]:
            await channel.send(f"🟢 BULLISH: {pair} at {key_low:.4f}")
        # Bearish Engulfing
        elif df['High'].iloc[-1] >= key_high and df['Open'].iloc[-1] > df['Close'].iloc[-1] and df['Close'].iloc[-1] < df['Open'].iloc[-2]:
            await channel.send(f"🔴 BEARISH: {pair} at {key_high:.4f}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    scan_market.start()

client.run(TOKEN)

import discord
from discord.ext import commands
import yfinance as yf
import asyncio

# --- PASTE YOUR DETAILS HERE ---
DISCORD_TOKEN = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"
CHANNEL_ID = 1518320481445613760 # Paste the ID you just copied
# ------------------------------

SYMBOLS = ['USDJPY=X', 'EURJPY=X', 'AUDJPY=X']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def check_markets():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    
    # Check if the ID is valid
    if not channel:
        print(f"CRITICAL ERROR: Could not find channel with ID {CHANNEL_ID}. Please double-check it.")
        return

    while not bot.is_closed():
        for symbol in SYMBOLS:
            try:
                # The user_agent is the key to preventing "No data found"
                data = yf.download(
                    symbol, 
                    period="1d", 
                    interval="5m", 
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                )
                
                if not data.empty:
                    last_price = data['Close'].iloc[-1].item()
                    message = f"Market Update for {symbol}: {last_price:.4f}"
                    await channel.send(message)
                    print(f"Sent: {message}")
                else:
                    print(f"No data found for {symbol} (Market may be closed)")
            except Exception as e:
                print(f"Error checking {symbol}: {e}")
        
        # Wait 5 minutes before the next round
        await asyncio.sleep(300)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Bot is now watching the markets and will post to channel {CHANNEL_ID}')
    bot.loop.create_task(check_markets())

bot.run(DISCORD_TOKEN)

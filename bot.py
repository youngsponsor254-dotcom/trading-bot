import requests

# 1. Configuration
fvg_top = 1.32281
fvg_bottom = 1.32110
webhook_url = "https://discord.com/api/webhooks/1518322612260835408/EPwi1MJA3QMQldKh3hohFD-nIg2ahtfcX3X0zr4b2XkbDf3Fbw0BExCI4-AvSsc9KQtR"

def send_discord_alert(message):
    data = {"content": message}
    requests.post(webhook_url, json=data)

# 2. Get live data
url = "https://api.frankfurter.app/latest?from=GBP&to=USD"
response = requests.get(url)
data = response.json()
latest_price = data['rates']['USD']

# 3. Check status
if latest_price >= fvg_bottom and latest_price <= fvg_top:
    msg = f"SIGNAL READY! Price: {latest_price:.5f}. LOOK FOR BUY."
    send_discord_alert(msg)
    print(msg)
elif latest_price < fvg_bottom:
    print(f"Latest Price: {latest_price:.5f} - WAITING (Price below zone)")
else:
    print(f"Latest Price: {latest_price:.5f} - WAITING (Price above zone)")

import requests

# Paste your URL here again, very carefully
webhook_url = "https://discord.com/api/webhooks/YOUR_ACTUAL_ID_HERE"

def test_discord():
    try:
        data = {"content": "🤖 TESTING: If you see this, the bot is connected!"}
        response = requests.post(webhook_url, json=data, timeout=10)
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 204:
            print("Success! Message sent.")
        else:
            print("Failed to send. Please check your URL.")
    except Exception as e:
        print(f"Error: {e}")

test_discord()

import os
from dotenv import load_dotenv
import requests
from send_email import send_email

load_dotenv(".env")

api_base_url = os.getenv("API_BASE_URL")
key = os.getenv("API_KEY")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
receiver = os.getenv("RECEIVER")

topic = "tesla"

api_url = f"{api_base_url}?apiKey={key}&q={topic}&from=2025-07-22&sortBy=publishedAt&language=en&pageSize=20"

print(api_url)

req = requests.get(api_url, timeout=5000)
data = req.json()

msg = "Subject: Latest news" + "\n"
for article in data["articles"]:
    if article["title"] and article["description"]:
        msg += (
            article["title"]
            + "\n"
            + article["description"]
            + "\n"
            + article["url"]
            + 2 * "\n"
        )

msg = msg.encode("utf-8")

send_email(username, password, receiver, msg)

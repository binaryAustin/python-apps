import smtplib, ssl
import os
import time
import sqlite3
from dotenv import load_dotenv
import requests
import selectorlib

load_dotenv(".env")

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

YAML_PATH = "extract.yaml"
EMPTY_TEXT = "no upcoming tours"
DATA_PATH = "data.txt"

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")

connection = sqlite3.connect("/root/data.db")


def scrape(url: str) -> str:
    """Scrape the page source from the URL."""
    res = requests.get(url, timeout=10.0, headers=HEADERS)
    source = res.text
    return source


def extract(source: str) -> str:
    extractor = selectorlib.Extractor.from_yaml_file(YAML_PATH)
    value: str = extractor.extract(source)["tours"]
    return value


def send_email(username: str, password: str, receiver: str, message: str):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def store(value: str):
    row = value.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(value: str):
    row = value.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date)
    )
    result = cursor.fetchone()
    return result


def main():
    while True:
        source = scrape(URL)
        extracted_value = extract(source)
        if extracted_value.lower() != EMPTY_TEXT:
            result = read(extracted_value)
            if not result:
                store(extracted_value)
                # msg = "Subject: New event coming up\n" + extracted_value
                # send_email(USERNAME, PASSWORD, RECEIVER, msg)
        time.sleep(30.0)


if __name__ == "__main__":
    main()

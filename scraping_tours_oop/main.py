import smtplib
import ssl
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
DB_PATH = "data.db"

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")


class Event:
    def scrape(self, url: str) -> str:
        """Scrape the page source from the URL."""
        res = requests.get(url, timeout=10.0, headers=HEADERS)
        source = res.text
        return source

    def extract(self, source: str) -> str:
        extractor = selectorlib.Extractor.from_yaml_file(YAML_PATH)
        value: str = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, username: str, password: str, receiver: str, message: str):
        host = "smtp.gmail.com"
        port = 465
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)


class Database:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)

    def store(self, value: str):
        row = value.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read(self, value: str):
        row = value.split(",")
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM events WHERE band=? AND city=? AND date=?",
            (band, city, date),
        )
        result = cursor.fetchone()
        return result


def main():
    db = Database(db_path=DB_PATH)
    event = Event()
    email = Email()
    while True:
        source = event.scrape(URL)
        extracted_value = event.extract(source)
        if extracted_value.lower() != EMPTY_TEXT:
            result = db.read(extracted_value)
            if not result:
                db.store(extracted_value)
                # msg = "Subject: New event coming up\n" + extracted_value
                # email.send(USERNAME, PASSWORD, RECEIVER, msg)
        time.sleep(30.0)


if __name__ == "__main__":
    main()

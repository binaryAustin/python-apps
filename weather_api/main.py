from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

prefix = "/api/v1"


def parse_filename(station: str) -> str:
    return "data_small/TG_STAID" + station.zfill(6) + ".txt"


stations = pd.read_csv("data_small/stations.txt", skiprows=17)[
    ["STAID", "STANAME                                 "]
]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route(f"{prefix}/<station>/<date>")
def findByDate(station: str, date: str):
    filename = parse_filename(station)
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10

    return {"station": station, "date": date, "temperature": temperature}


@app.route("/api/v1/<station>")
def findByStation(station: str):
    filename = parse_filename(station)
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/year/<station>/<year>")
def findByYear(station: str, year: str):
    filename = parse_filename(station)
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(year)].to_dict("records")
    return result


if __name__ == "__main__":
    app.run(debug=True, port=4200, host="0.0.0.0")

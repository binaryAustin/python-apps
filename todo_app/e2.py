import csv

with open("weather.csv", "r", encoding="utf8") as fr:
    data = list(csv.reader(fr))


city = input("Enter a city: ")


for row in data[1:]:
    if row[0] == city:
        print(row[1])

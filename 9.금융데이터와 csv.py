stocks = [
    {"date": "2026-09-01", "name": "삼성전자", "close": 70000},
    {"date": "2026-09-02", "name": "삼성전자", "close": 72000},
    {"date": "2026-09-03", "name": "삼성전자", "close": 71000}
]

import csv

with open("stock.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["date", "name", "close"])

    for stock in stocks:
        writer.writerow([
            stock["date"],
            stock["name"],
            stock["close"]
        ])
import csv

stocks = []

with open("stock.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    header = next(reader)

    for row in reader:
        stock = {
            "date": row[0],
            "name": row[1],
            "close": int(row[2])
        }

        stocks.append(stock)


total = 0

for stock in stocks:
    total += stock["close"]

average = total / len(stocks)

print(f"평균 price : {average:,.0f}원")
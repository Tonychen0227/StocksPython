import requests
from urllib.request import urlopen
import datetime
import os
import json
import pandas as pd
import csv

collection = {}

initialized = False
columnsWritten = False

APIPartOne = "https://cloud.iexapis.com/stable/stock/"
APIPartTwo = "/chart/3m?token=" + os.getenv("IEX_TOKEN")

with open('./nasdaqlisted.txt') as f:
    content = f.readlines()

outfile = open("./stocksDumpJul16.csv", "w")
wr = csv.writer(outfile, dialect='excel')

for row in content:
    if not initialized:
        initialized = True
        continue
    row = str(row).split("|")
    symbol = row[0]
    response = requests.get(APIPartOne + symbol + APIPartTwo)
    print(symbol)
    if response.status_code != 200:
        continue
    snippet = json.loads(response.text)
    if (len(snippet) < 63):
        continue
    index = 0
    for x in snippet:
        if index == 0:
            collection[symbol] = {}
            collection[symbol]["Symbol"] = symbol
        collection[symbol][str(index) + " open"] = x["open"]
        ""
        collection[symbol][str(index) + " close"] = x["close"]
        collection[symbol][str(index) + " high"] = x["high"]
        collection[symbol][str(index) + " low"] = x["low"]
        collection[symbol][str(index) + " volume"] = x["volume"]
        index = index + 1
    if not columnsWritten:
        wr.writerow(list(collection[symbol].keys()))
        columnsWritten = True
    wr.writerow(list(collection[symbol].values()))
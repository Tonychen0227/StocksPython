import csv
import requests
import datetime
import os
import json

todayDate = datetime.date.today()
APIPartOne = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
APIPartTwo = "&outputsize=compact&datatype=csv&apikey=" + os.getenv('ALPHA_VANTAGE_TOKEN')

GoodStocks = {}
initialized = False

# ALL STOCKS
data = open('nasdaqtraded.txt', 'r')
counter = 0
for row in data:
    counter += 1
    if (counter > 10):
        break;
    row = str(row).split("|")
    symbol = row[0]
    if initialized:
        try:
            print(APIPartOne + symbol + APIPartTwo)
            response = requests.get(APIPartOne + symbol + APIPartTwo)
            reader = csv.reader(response.text.split('\n'))
            reader.__next__()
            today = reader.__next__()
            yesterday = reader.__next__()
            print(symbol)
            MA20 = float(yesterday[4]) + float(today[4])
            MA50 = float(yesterday[4]) + float(today[4])
            MA90 = float(yesterday[4]) + float(today[4])
            try:
                for x in range(0, 88):
                    lastday = reader.__next__()
                    if x < 18:
                        MA20 = MA20 + float(lastday[4])
                    if x < 48:
                        MA50 = MA50 + float(lastday[4])
                    MA90 = MA90 + float(lastday[4])
                MA20 = MA20 / 20
                MA50 = MA50 / 50
                MA90 = MA90 / 90
            except:
                MA20 = 100
                MA50 = 50
                MA90 = 0
            if float(today[4]) > 1:
                if float(today[4]) / float(yesterday[4]) > 1.05 and float(today[5]) / float(yesterday[5]) > 1.5 and (
                        MA20 >= MA50 >= MA90):
                    print('good')
                    GoodStocks[symbol] = {'increase_price': round((float(today[4]) / float(yesterday[4])), 2),
                                          'increase_volume': round((float(today[5]) / float(yesterday[5])), 2),
                                          'new stock': (MA20 == 100 and MA50 == 50 and MA90 == 0),
                                          'MA20': round(MA20, 2),
                                          'MA50': round(MA50, 2),
                                          'MA90': round(MA90, 2),
                                          'previous instances last 30 days': 1}
        except:
            pass
    else:
        initialized = True

reports_dir = "reports/" + str(todayDate)[0:7]

if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)

for symbol in GoodStocks.keys():
    for x in range(1, 30):
        try:
            data = open(reports_dir + "/" + str(todayDate - datetime.timedelta(x)) + ".txt", "r").read()
            data = data.split("\n")
            for row in data:
                name = row.split(":")[0]
                if name == symbol:
                    GoodStocks[symbol]['previous instances last 30 days'] = GoodStocks[symbol]['previous instances last 30 days'] + 1
        except FileNotFoundError:
            pass

results = open(reports_dir + "/" + str(todayDate) + ".txt", "w+")
SectorReport = requests.get("https://www.alphavantage.co/query?function=SECTOR&datatype=csv&apikey=" + os.getenv('ALPHA_VANTAGE_TOKEN'))
SectorDictionary = json.loads(SectorReport.text)['Rank A: Real-Time Performance']

results.write("Good stocks today" + "\n")
for key in GoodStocks.keys():
    results.write(key + ": " + str(GoodStocks[key]) + "\n")
results.write("\n")


#SP500
GoodStocks = {}
initialized = False

with open("constituents_csv.csv", mode='r') as infile:
    reader = csv.reader(infile)
    counter = 0
    for row in reader:
        counter += 1
        if (counter > 10):
            break;
        symbol = row[0]
        if initialized:
            try:
                print(APIPartOne + symbol + APIPartTwo)
                response = requests.get(APIPartOne + symbol + APIPartTwo)
                reader = csv.reader(response.text.split('\n'))
                reader.__next__()
                today = reader.__next__()
                yesterday = reader.__next__()
                print(symbol)
                MA20 = float(yesterday[4]) + float(today[4])
                MA50 = float(yesterday[4]) + float(today[4])
                MA90 = float(yesterday[4]) + float(today[4])
                try:
                    for x in range(0, 88):
                        lastday = reader.__next__()
                        if x < 18:
                            MA20 = MA20 + float(lastday[4])
                        if x < 48:
                            MA50 = MA50 + float(lastday[4])
                        MA90 = MA90 + float(lastday[4])
                    MA20 = MA20 / 20
                    MA50 = MA50 / 50
                    MA90 = MA90 / 90
                except:
                    MA20 = 100
                    MA50 = 50
                    MA90 = 0
                if float(today[4]) > 1:
                    if float(today[4]) / float(yesterday[4]) > 1.05 and float(today[5]) / float(
                            yesterday[5]) > 1.5 and (
                            MA20 >= MA50 >= MA90):
                        print('good')
                        GoodStocks[symbol] = {'increase_price': round((float(today[4]) / float(yesterday[4])), 2),
                                              'increase_volume': round((float(today[5]) / float(yesterday[5])), 2),
                                              'new stock': (MA20 == 100 and MA50 == 50 and MA90 == 0),
                                              'MA20': round(MA20, 2),
                                              'MA50': round(MA50, 2),
                                              'MA90': round(MA90, 2),
                                              'previous instances last 30 days': 1}
            except:
                pass
        else:
            initialized = True

for symbol in GoodStocks.keys():
    for x in range(1, 30):
        try:
            data = open(reports_dir + "/" + str(todayDate - datetime.timedelta(x)) + ".txt", "r").read()
            data = data.split("\n")
            for row in data:
                name = row.split(":")[0]
                if name == symbol:
                    GoodStocks[symbol]['previous instances last 30 days'] = GoodStocks[symbol]['previous instances last 30 days'] + 1
        except FileNotFoundError:
            pass

results.write("Good SP500 stocks today" + "\n")
for key in GoodStocks.keys():
    results.write(key + ": " + str(GoodStocks[key]) + "\n")
results.write("\n")

results.write("Industry report for the day" + "\n")
for key in SectorDictionary.keys():
    results.write(key + ": " + SectorDictionary[key] + "\n")
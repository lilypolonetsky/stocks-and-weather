""" graph the standard deviation of the weather against the standard deviation of the avg stock price change """

import matplotlib.pyplot as plt
  
graph = plt.figure()

#get the standard deviation of the avg stock price change
stocks = {}

f = open("data/dji_price_changes.csv")
lines = f.readlines()
for line in lines:
    fields = line.split(',')
    date = fields[0]
    std = float(fields[1].rstrip())

    if date.split('-')[0] == '12' and date.split('-')[1] == '2019':
        continue

    stocks[date] = std
    
#get the standard deviation of the weather for the x values
weather = {}

f = open("data/tempDays.csv")
lines = f.readlines()

for line in lines:
    fields = line.split(',')
    date = fields[0]
    std = float(fields[1].rstrip())

    if date in list(stocks.keys()):
        weather[date] = std

plt.scatter(weather.values(), stocks.values(), s=.7)

plt.xlabel("weather")
plt.ylabel("stocks")

graph.savefig("priceToWeather.pdf")

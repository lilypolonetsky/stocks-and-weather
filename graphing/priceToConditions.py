import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages("PriceToConditions.pdf")

#get weather conditions
f = open("data/badConditions.csv")
lines = f.readlines()

badWeather = []
for line in lines:
    badWeather.append(line.split(',')[0])

g = open("data/dji_price_changes.csv")
lines = g.readlines()

badPrice = []
decreasePrice = []
increasePrice = []
for line in lines:
    fields = line.split(',')
    date = fields[0]
    std = fields[1]

    if float(std) < 0:
        decreasePrice.append(date)
        if float(std) <= -1:
            badPrice.append(date)
    else:
        increasePrice.append(date)

badWeatherPrice = [] #both bad weather and bad price 
notBadPrice = [] #bad weather, but not bad price
#find all dates where the price change is 1 standard deviation below the mean and the weather conditions are bad
for date in badWeather:
    if date in badPrice:
        badWeatherPrice.append(date)
    else:
        notBadPrice.append(date)

goodPriceGoodWeather = []
badPriceGoodWeather = []
#find all the dates where there is bad weather in the price increase and decrease list
for date in increasePrice:
    if date not in badWeather:
        increasePrice.remove(date)
        goodPriceGoodWeather.append(date)
for date in decreasePrice:
    if date not in badWeather: #date is decrease in price and good weather
        decreasePrice.remove(date)
        badPriceGoodWeather.append(date)
        

#of all the bad stock price days, was the weather bad?

#calculate sizes of each slice of pie
both = round(len(badWeatherPrice)/len(badWeather)*100)
notPrice = round(len(notBadPrice)/len(badWeather)*100) #not bad price, but bad weather

increase = round(len(increasePrice)/len(badWeather)*100)
decrease = round(len(decreasePrice)/len(badWeather)*100)

goodWeatherDays = len(goodPriceGoodWeather)+len(badPriceGoodWeather)
increaseGood = round(len(goodPriceGoodWeather)/goodWeatherDays*100)
decreaseGood = round(len(badPriceGoodWeather)/goodWeatherDays*100)
#chart 1- was there a significant decrease in price when there was bad weather conditions?
labels = 'significant decrease in price', 'no significant decrease in price'
sizes = [both,notPrice]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("Bad weather conditions", bbox={'facecolor':'0.8', 'pad':2})
plt.savefig(pp, format="pdf")

#chart 2- did the price increase or decrease when there was bad weather conditions?
labels = 'increase in price', 'decrease in price'
sizes = [increase,decrease]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("Bad weather conditions", bbox={'facecolor':'0.8', 'pad':2})

plt.savefig(pp, format="pdf")

#chart 3- did the price increase or decrease when there was not bad weather conditions?
labels = 'increase in price', 'decrease in price'
sizes = [increaseGood,decreaseGood]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("No Bad Weather Conditions", bbox={'facecolor':'0.8', 'pad':2})

plt.savefig(pp,format="pdf")

pp.close()

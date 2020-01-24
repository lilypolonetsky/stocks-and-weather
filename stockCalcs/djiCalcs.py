""" The purpose of this script is to find how many standard deviations from the month's mean each respective day's price change is. 

For example, suppose we have the following data set:
------------------------------------------------------------------------------------
|day          |  how did the price change?         | standard deviations from mean  |
------------------------------------------------------------------------------------
| 1           | -5                                 | (-5-5.75)/9.038 = -1.189       |
------------------------------------------------------------------------------------
| 2           | 5                                  | (5-5.75)/9.038 = -0.083        |
------------------------------------------------------------------------------------
| 3           | 3                                  | (3-5.75)/9.038 = -0.304        |
------------------------------------------------------------------------------------
| 4           | 20                                 | (20-5.75)/9.038 = 1.577        |
------------------------------------------------------------------------------------
mean price change: 5.75, standard deviation: 9.038

Process:
- open dji.csv
- create a dictionary to capture the data with the format {mnth-yr: {day: close-open, day:close-open}}
- calculate each month's mean and std and store it in a dictionary called month_stats with the format {mnth-yr: [mean, std]}
- create a file to put mnth-yr-day, std from the month's mean
- loop through the dictionary with the data and calculate for each day, how far it is from its month's mean
"""
import numpy as np

#input: line which is a line of a file
#output: array holding info from line in format [mnth,yr,day,closePrice,openPrice]
def captureData(line):
    fields = line.split(',')
    date = fields[0].split('-')

    yr = date[0]
    mnth = date[1]
    day = date[2]
    openPrice = fields[1]
    closePrice = fields[3]

    return [mnth,yr,day,closePrice,openPrice]

#takes data in format from function captureData
#returns (key,{day:close-open})
def createEntry(fields):
    key = fields[0]+"-"+fields[1] #mnth-yr
    closePrice = float(fields[3])
    openPrice = float(fields[4])
    value = {fields[2]:closePrice-openPrice}
    return key,value

def calc_month_stats(priceChanges):
    return [np.mean(priceChanges),np.std(priceChanges)]

def std_from_mean(priceChange,mnth_mean,mnth_std):
    price = float(priceChange)
    numerator = round(price-mnth_mean,3)
    ans = round(numerator/mnth_std,3)
    return ans

#open the data file
myFile = open("../data/dji.csv")
lines = myFile.readlines()

data = {} #{mnth-yr: {day:close-open, day:close-open}}
firstLine = True
#create a dictionary to capture the data with the format {mnth-yr: {day: close-open, day:close-open}}
for line in lines:

    #skip the header row
    if firstLine:
        firstLine = False
        continue
    
    fields = captureData(line) #capture the data in form [mnth,yr,day,closePrice,openPrice]
    entry = createEntry(fields) #format the data for dictionary entry

    #place entry into the data dictionary
    if entry[0] not in data: #does the key exist yet?
        data[entry[0]] = entry[1]
    else:
        data[entry[0]].update(entry[1])


#get the month's mean and standard deviation
month_stats = {} #{mnth-yr:[mean,std]}
for mnth_yr in data:
    priceChanges = data[mnth_yr].values()
    priceChanges = [int(i) for i in priceChanges]
    
    month_stats[mnth_yr] = calc_month_stats(priceChanges)

#file with format mnth-yr,standard deviations from month's mean
g = open("../data/dji_price_changes.csv","w")

#loop through each day's price change
for mnth_yr in data:
    mnth_mean = month_stats[mnth_yr][0] #get the month's mean
    mnth_std = month_stats[mnth_yr][1] #get the month's standard deviation

    for day in data[mnth_yr]:
        priceChange = data[mnth_yr][day]
        std = std_from_mean(priceChange,mnth_mean,mnth_std)
        g.write(mnth_yr+"-"+day+","+str(std)+"\n")

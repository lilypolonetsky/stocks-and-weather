""" This script outputs all dates which has a mean temperature that is one standard deviation below the month's mean --> outputs to file all "colder" weather days.

Process:
- open file
- create a dictionary with {month-year:{day:[temp,temp,temp]} with each temp in array coming from each hour recorded
- for each line:
  - split the fields
  - get date field (field 1)
  - get temp field (field 7)
  - add the temperature to the dictionary
- create month stats array with {month-year:[mean, std]}
- for each month-year in dictionary:
  - create empty temp array
  - for each day 
    - calculate the mean temperature for the day and append it to the end of the list that hosts the temps for the day
    - save the mean from each day in temp array
    - when last day, calculate month mean and standard deviation from temp array and save this in month stats array
"""
import gzip
import numpy as np

f = gzip.open('../data/manhattanHistoricalWeather/manhattanWeather.csv.gz','rt')
lines = f.readlines()

temp_dict = {} #{month-year:{day:[temp,temp,temp]} with each temp in array coming from each hour recorded

month_stats = {} # {month-year:[mean, std]}

firstLine = True
for line in lines: #loop through file
    if firstLine:
        firstLine = False
        continue
    fields = line.split(',')
    dateFields = fields[1].split('-')
    
    year = dateFields[0]
    month = dateFields[1]
    day = dateFields[2][:2]
    temp = float(fields[7])
    
    key = month+'-'+year

    #populate dictionary
    if key not in temp_dict:
        temp_dict[key] = {day:[temp]}
    elif day not in temp_dict[key]:
        temp_dict[key].update({day:[temp]})
    else:
        temp_dict[key][day].append(temp)

f.close()

#calculate each day's mean
for mnthYearKey in temp_dict:
    tempArray = [] #save each day in month's mean

    month_dict = temp_dict[mnthYearKey]
    
    for dayKey in month_dict:
        mean = np.mean(month_dict[dayKey])
        month_dict[dayKey].append(mean) #last value now holds mean for the day's temp
        tempArray.append(mean)

        if len(month_dict.keys()) == int(dayKey):
            month_mean = np.mean(tempArray)
            month_std = np.std(tempArray)
            month_stats[mnthYearKey] = [month_mean,month_std]

i = open("../data/tempDays.csv","w") #file that holds all the days temperatures and std
h = open("../data/badTempDays.csv", "w") #file that holds days where temp is 1 std below mean

for mnthYear in temp_dict:
    days = temp_dict[mnthYear]
    mnth_mean = int(month_stats[mnthYear][0])
    mnth_std = int(month_stats[mnthYear][1])
    one_below_mean = mnth_mean - mnth_std
    
    for day in days: #{day:[temp,temp,meanTemp]}
        std_below_mean = round(round(days[day][-1]-mnth_mean,3)/round(mnth_std,3),3)
        i.write(mnthYear+"-"+day+","+str(std_below_mean)+"\n")

        if days[day][-1] <= one_below_mean:
            h.write(mnthYear+"-"+day+","+str(std_below_mean)+"\n")

h.close()
        

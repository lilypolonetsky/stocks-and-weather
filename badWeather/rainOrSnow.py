""" This script looks through the weather data found in data/manhattanHistoricalWeather and finds all the days where either snow or heavy snow is described (not light snow) or rain that is described as moderate or heavy intensity 
Process:
- open file
- loop through lines
- cut line into fields
- capture field 31 (description of weather)
- if the weather is described as either "moderate rain", "heavy intensity rain", "thunderstorm with rain", "heavy snow", or "snow" then save the date into a dictionary (if not already there)
"""
import gzip

f = gzip.open('../data/manhattanHistoricalWeather/manhattanWeather.csv.gz','rt')
lines = f.readlines()

weatherChoices = ["moderate rain","heavy intensity rain", "thunderstorm with rain", "heavy snow", "snow"]

rainSnowDays = {} #{mnth-yr-day:[descrip,descrip]}

firstLine = True
for line in lines:
    if firstLine:
        firstLine = False
        continue

    fields = line.split(',')
    weatherDescrip = fields[31]
    dateInfo = fields[1].split('-')
    year = dateInfo[0]
    month = dateInfo[1]
    day = dateInfo[2][:2]
    mnth_yr_day = month+"-"+year+"-"+day

    if weatherDescrip in weatherChoices: #check if weather qualifies as "bad"
        #check if date is already stored
        if mnth_yr_day not in rainSnowDays:
            rainSnowDays[mnth_yr_day] = [weatherDescrip]
        elif weatherDescrip not in rainSnowDays[mnth_yr_day]: #check if description not stored for that date
            rainSnowDays[mnth_yr_day].append(weatherDescrip)

f.close()

#open file to write info to
h = open("../data/badConditions.csv","w")

for key in rainSnowDays:
    descrip = ' and '.join(rainSnowDays[key])
    h.write(key+","+descrip+"\n")

h.close()

# Clean up the data, by turning it into pipe-delimited, and by
# turning the UTC data into local time.

#dt,dt_iso,timezone,city_id,city_name,lat,lon,temp,temp_min,temp_max,pressure,sea_level,grnd_level,humidity,wind_speed,wind_deg,rain_1h,rain_3h,rain_6h,rain_12h,rain_24h,rain_today,snow_1h,snow_3h,snow_6h,snow_12h,snow_24h,snow_today,clouds_all,weather_id,weather_main,weather_description,weather_icon
#946684800,2000-01-01 00:00:00 +0000 UTC,-18000,5125771,Manhattan,40.783428,-73.966248,35.11,33.08,37.94,1020.7,,,85,5.82,210,0,,0,,,,,,,,,,20,801,Clouds,few clouds,02n

import datetime

# read and then print out the header as pipe delimited
line = input()
fields = line.split(',')
fields[1] = 'dtNYC'
print('|'.join(fields))

line = input()
while line:
    # the raw data is comma-delimited
    fields = line.split(',')

    # field 1 has UTC date and time, and field 2 has the number of seconds to
    # add to UTC to get the date and time in the local time zone in which
    # this data was collected
    utcTime = fields[1][:19]
    timeZoneDelta = int(fields[2])

    # parse the UTC date and time
    dt = datetime.datetime.strptime(utcTime, "%Y-%m-%d %H:%M:%S")

    # add the number of seconds from field 2 to get the local time
    localTime = dt + datetime.timedelta(0, timeZoneDelta)

    # insert back into field 1 the local time, along with the day of week: i.e. Sun, Mon, Tue, Wed
    fields[1] = localTime.strftime("%Y-%m-%d %H:%M:%S %a")

    # print out the record as pipe delimited
    print('|'.join(fields))

    # read the next line from stdin
    try: line = input()
    except: line = None

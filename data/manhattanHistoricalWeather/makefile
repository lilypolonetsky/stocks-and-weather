manhattanWeatherClean.gz:	cleanData.py manhattanWeather.csv.gz
	zcat manhattanWeather.csv.gz | python3 ./cleanData.py | gzip -9 >manhattanWeatherClean.gz

clean:
	rm manhattanWeatherClean.gz



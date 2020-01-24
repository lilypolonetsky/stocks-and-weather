all: graphing/priceToWeather.pdf graphing/PriceToConditions.pdf

clean:
	rm data/dji_price_changes.csv data/dji_decrease.csv data/badConditions.csv data/badTempDays.csv data/tempDays.csv graphing/priceToWeather.pdf graphing/PriceToConditions.pdf

data/dji_price_changes.csv: data/dji.csv stockCalcs/djiCalcs.py
	python3 stockCalcs/djiCalcs.py

data/dji_decrease.csv: data/dji_price_changes.csv stockCalcs/significantDecrease.py
	python3 stockCalcs/significantDecrease.py

data/badTempDays.csv: data/manhattanHistoricalWeather/manhattanWeather.csv.gz badWeather/badTemp.py
	python3 badWeather/badTemp.py

graphing/priceToWeather.pdf: data/dji_price_changes.csv data/tempDays.csv graphing/priceToWeather.py
	python3 graphing/priceToWeather.py

data/badConditions.csv: badWeather/rainOrSnow.py data/manhattanHistoricalWeather/manhattanWeather.csv.gz
	python3 badWeather/rainOrSnow.py

graphing/PriceToConditions.pdf: graphing/priceToConditions.py data/badConditions.csv data/dji_price_changes.csv
	python3 graphing/priceToConditions.py

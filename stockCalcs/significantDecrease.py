""" how often is there a significant decrease in price? """
g = open("../data/dji_decrease.csv","w")
f = open("../data/dji_price_changes.csv")
lines = f.readlines()

for line in lines:
    fields = line.split(',')
    std = float(fields[1])

    if std <= -1:
        g.write(fields[0]+","+str(std)+"\n")
        

import random
import csv

uacsv 	= open('useragents.csv','r')
ualist 	= csv.reader(uacsv)
ualist 	= [row for row in ualist]
ualist 	= [i[0] for i in ualist]
random.shuffle(ualist)

def load():
	return {'User-Agent': random.choice(ualist)}
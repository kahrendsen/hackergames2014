import csv

with open('raw_history.csv', 'rb') as f:

    reader = csv.DictReader(f, delimiter='|', quotechar='"')
    for row in reader:
        print row
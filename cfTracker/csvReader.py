import csv
from django.conf import settings
import os

f = open(os.path.join(settings.BASE_DIR, 'data/food-footprints.csv'), 'r')
reader = csv.reader(f)
columns = []
data = {}
for i, row in enumerate(reader):
    if i == 0:
        columns = row
        continue

    data[row[0]] = {}
    for j in range(1, len(row)):
        data[row[0]][columns[j]] = row[j]

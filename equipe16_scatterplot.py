import csv
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser

x = [] # file names
y = [] # Date
z = [] # Authors
i = 0

with open('partie2/data_gpslogger.csv') as csvFile:
    reader = csv.reader(csvFile)
    next(reader)
    for row in reader:
        x.append(row[0].split('/')[-1])
        y.append(parser.parse(row[2]))
        z.append(row[1])
color_mapping = dict()
for author in z:
    if author in color_mapping:
        continue
    else:
        color_mapping[author] = i
        i += 1

color_array = [ color_mapping[j] for j in z ]
plt.figure(figsize=(30,30))
plt.scatter(x, y, c=color_array, zorder=1)
plt.xticks(rotation=90)
plt.gca().set_axisbelow(True)
plt.gca().set_xticklabels([])
plt.gca().set_xlabel('Files')
plt.gca().set_ylabel('Time')
plt.grid()
plt.savefig('gpslogger.pdf',bbox_inches='tight')
# plt.show()
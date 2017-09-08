import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates



dates =  []
values = []

with open('PerformanceLogData_1user.csv') as performanceLogData:
  csvReader = csv.reader(performanceLogData)
  for row in csvReader:
    if row[1] == '492':
      date = datetime.datetime.fromtimestamp(int(row[2]))
      dates.append(date)
      values.append(row[3])

# print len(dates)
# print len(values)

fig, ax = plt.subplots()
ax.plot(dates, values)


# format the ticks
# ax.xaxis.set_major_locator(years)
# ax.xaxis.set_major_formatter(yearsFmt)
# ax.xaxis.set_minor_locator(months)

ax.set_ylim(0,5)

ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.format_ydata = values
# ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()


plt.xlabel('Dates')
plt.ylabel('Values')
plt.title('User 4349, Parameter 492')
plt.grid(True)
plt.savefig("user4349_param492.png")
plt.show()
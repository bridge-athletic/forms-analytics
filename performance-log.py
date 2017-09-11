import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates


dates =  []
values = []

##################### one user, one parameter #####################


# ## open csv with performance log data for one athlete
# with open('PerformanceLogData_1user.csv') as performanceLogData:
#   csvReader = csv.reader(performanceLogData)
#   for row in csvReader:
#     if row[1] == '492':
#       ## select data matching one parameter
#       date = datetime.datetime.fromtimestamp(int(row[2]))
#       dates.append(date)
#       values.append(row[3])

# ## initialize the plot
# fig, ax = plt.subplots()
# ax.plot(dates, values)
# ax.grid(True)

# ax.set_ylim(0,5.5)

# ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# ax.format_ydata = values

# fig.autofmt_xdate()

# ## set axes and title
# ax.set_xlabel('Dates')
# ax.set_ylabel('Values')
# ax.set_title('User 4349, Parameter 492')
# plt.show()




##################### one user, all (scored) parameters #####################


# ## open csv with performance log data for one athlete
# with open('PerformanceLogData_1user.csv') as performanceLogData:
#   csvReader = csv.reader(performanceLogData)
#   for row in csvReader:
#     date = datetime.date.fromtimestamp(int(row[2]))
#     ## do not include weight or hours of sleep
#     if (row[1] == '2') or (row[1] == '614'):
#       continue 
#     else:
#       ## check if date in the dates array
#       if (date in dates):
#         i = dates.index(date)
#         values[i] = values[i] + (int(row[3]))
#       else:
#         dates.append(date)
#         values.append(int(row[3]))

# ## some of the data is corrupted, want to exlude these points
# remove = []
# for value in values:
#   if value > 35:
#     remove.append(value)
# for val in remove:
#   idx = values.index(val)
#   del values[idx]
#   del dates[idx]

# ## initialize the plot
# fig, ax = plt.subplots()
# ax.plot(dates, values)
# ax.grid(True)

# ax.set_ylim(0,37)

# ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# ax.format_ydata = values

# fig.autofmt_xdate()

# ## set axes and title
# ax.set_xlabel('Dates')
# ax.set_ylabel('Values')
# ax.set_title('User 4349, Form Score')
# plt.show()




##################### one user, submissions over #####################


## open csv with performance log data for one athlete
with open('PerformanceLogData_1user.csv') as performanceLogData:
  csvReader = csv.reader(performanceLogData)
  for row in csvReader:
    date = datetime.date.fromtimestamp(int(row[2]))
    dates.append(date)

u_dates = np.unique(dates)

submissions = 0
for date in u_dates:
  submissions += 1
  values.append(submissions)

print dates
print values

## initialize the plot
fig, ax = plt.subplots()
ax.plot(u_dates, values)
ax.grid(True)

ax.set_ylim(0,100)

ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.format_ydata = values

fig.autofmt_xdate()

## set axes and title
ax.set_xlabel('Dates')
ax.set_ylabel('Values')
ax.set_title('Submissions for User 4349')
plt.show()
























import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

from Graph import *

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
#       values.append(int(row[3]))

# # g = Graph('line', 'User 4349, Parameter 492', 5.5, 'Dates', 'Param Score', dates, values)
# g = Graph('histogram', 'User 4349, Parameter 492', 5.5, 'Dates', 'Param Score', dates, values)
# g.buildGraph()




##################### one user, all (scored) parameters #####################


## open csv with performance log data for one athlete
with open('PerformanceLogData_1user.csv') as performanceLogData:
  csvReader = csv.reader(performanceLogData)
  for row in csvReader:
    date = datetime.date.fromtimestamp(int(row[2]))
    ## do not include weight or hours of sleep
    if (row[1] == '2') or (row[1] == '614'):
      continue 
    else:
      ## check if date in the dates array
      if (date in dates):
        i = dates.index(date)
        values[i] = values[i] + (int(row[3]))
      else:
        dates.append(date)
        values.append(int(row[3]))

## some of the data is corrupted, want to exlude these points
remove = []
for value in values:
  if value > 35:
    remove.append(value)
for val in remove:
  idx = values.index(val)
  del values[idx]
  del dates[idx]

# g = Graph('line', 'User 4349, Form Score', 37, 'Dates', 'Form Score', dates, values)
g = Graph('histogram', 'User 4349, Form Score', 37, 'Dates', 'Form Score', dates, values)

g.buildGraph()


##################### one user, submissions over #####################


# # open csv with performance log data for one athlete
# with open('PerformanceLogData_1user.csv') as performanceLogData:
#   csvReader = csv.reader(performanceLogData)
#   for row in csvReader:
#     date = datetime.date.fromtimestamp(int(row[2]))
#     dates.append(date)

# u_dates = np.unique(dates)

# submissions = 0
# for date in u_dates:
#   submissions += 1
#   values.append(submissions)

# g = Graph('line', 'User 4349, Form Submissions', 100, 'Dates', 'Form Submissions', u_dates, values)
# g.buildGraph()
























# SELECT userId, parameterId, UNIX_TIMESTAMP(recordedAt), intValue 
# FROM userparameter 
# WHERE userId in (4349) 
# AND formquestionid in (103, 104, 105, 106, 107, 108, 109) 
# LIMIT 100000;

import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

## this can be scaled to include many athletes
individualPerformanceLogData = {
  "fatigue": {
    "dates": [],
    "values": []
  },
  "soreness": {
    "dates": [],
    "values": []
  },
  "stress": {
    "dates": [],
    "values": []
  },
  "sleep": {
    "dates": [],
    "values": []
  },
  "nutrition": {
    "dates": [],
    "values": []
  },
  "hydration": {
    "dates": [],
    "values": []
  },
  "overall": {
    "dates": [],
    "values": []
  }
}

# takes a file with performance log data for one user 
def parseDataFromCSV(filename):

  with open(filename) as performanceLogData:
    csvReader = csv.reader(performanceLogData)
    for row in csvReader:
      ## convert date to YYYY-MM-DD
      date = datetime.date.fromtimestamp(int(row[2]))
      
      ## fatigue data; parameterId 492
      if (int(row[1]) == 492):
        individualPerformanceLogData["fatigue"]["dates"].append(date)
        individualPerformanceLogData["fatigue"]["values"].append(int(row[3]))
      
      ## soreness data; parameterId 493
      if (int(row[1]) == 493):
        individualPerformanceLogData["soreness"]["dates"].append(date)
        individualPerformanceLogData["soreness"]["values"].append(int(row[3]))
      
      ## stress data; parameterId 494
      if (int(row[1]) == 494):
        individualPerformanceLogData["stress"]["dates"].append(date)
        individualPerformanceLogData["stress"]["values"].append(int(row[3]))
      
      ## sleep data; parameterId 495
      if (int(row[1]) == 495):
        individualPerformanceLogData["sleep"]["dates"].append(date)
        individualPerformanceLogData["sleep"]["values"].append(int(row[3]))
      
      ## nutrition data; parameterId 496
      if (int(row[1]) == 496):
        individualPerformanceLogData["nutrition"]["dates"].append(date)
        individualPerformanceLogData["nutrition"]["values"].append(int(row[3]))
      
      ## hydration data; parameterId 497
      if (int(row[1]) == 497):
        individualPerformanceLogData["hydration"]["dates"].append(date)
        individualPerformanceLogData["hydration"]["values"].append(int(row[3]))
      
      ## overall data; parameterId 498
      if (int(row[1]) == 498):
        individualPerformanceLogData["overall"]["dates"].append(date)
        individualPerformanceLogData["overall"]["values"].append(int(row[3]))


def individualParamTrend(params):
  ## initialize the plot
  fig, ax = plt.subplots()
  graphTitle = "Individual (userId 4349) Trends for "

  ## add all params indicated by user
  ## each block adds a new plot to the figure
  if (params['fatigue'] == 'true'):
    dates = individualPerformanceLogData["fatigue"]["dates"]
    values = individualPerformanceLogData["fatigue"]["values"]
    ax.plot(dates, values, label='fatigue')
    graphTitle += 'Fatigue '

  if (params['soreness'] == 'true'):
    dates = individualPerformanceLogData["soreness"]["dates"]
    values = individualPerformanceLogData["soreness"]["values"]      
    ax.plot(dates, values, label='soreness')
    graphTitle += 'Soreness '

  if (params['stress'] == 'true'):
    dates = individualPerformanceLogData["stress"]["dates"]
    values = individualPerformanceLogData["stress"]["values"] 
    ax.plot(dates, values, label='stress')
    graphTitle += 'Stress '

  if (params['sleep'] == 'true'):
    dates = individualPerformanceLogData["sleep"]["dates"]
    values = individualPerformanceLogData["sleep"]["values"] 
    ax.plot(dates, values, label='sleep')
    graphTitle += 'Sleep '

  if (params['hydration'] == 'true'):
    dates = individualPerformanceLogData["hydration"]["dates"]
    values = individualPerformanceLogData["hydration"]["values"] 
    ax.plot(dates, values, label='hydration')
    graphTitle += 'Hydration '

  if (params['nutrition'] == 'true'):
    dates = individualPerformanceLogData["nutrition"]["dates"]
    values = individualPerformanceLogData["nutrition"]["values"] 
    ax.plot(dates, values, label='nutrition')
    graphTitle += 'Nutrition '

  if (params['overall'] == 'true'):
    dates = individualPerformanceLogData["overall"]["dates"]
    values = individualPerformanceLogData["overall"]["values"] 
    ax.plot(dates, values, label='overall')
    graphTitle += 'Overall '

  ax.grid(True)
  ax.set_ylim(0, 5.5)   ## setting to 5.5 to give room at the top of the graph
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Values')
  ax.set_title(graphTitle)
  
  plt.show()


def athleteFormScore(data):

  fig, ax = plt.subplots()
  graphTitle = "Individual (userId 4349) Form Score"
  dates = data["dates"]
  values = data["values"]
  ax.plot(dates, values, label='Form Score')

  ax.grid(True)
  ax.set_ylim(0, 38)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Form Score (total)')
  ax.set_title(graphTitle)

  plt.show()
  



def requestIndividualParamTrend():
  ## Data needs to be organized and parsed 
  parseDataFromCSV('Individual_performance_log_data.csv')

  # initialize all to false
  graphParams = {
    'sleep': 'false',
    'hydration': 'false',
    'nutrition': 'false',
    'stress': 'false',
    'fatigue': 'false',
    'soreness': 'false',
    'overall': 'false',
    'formscore': 'false'
  }

  ## Prompting user to input the specific params they want to see
  print
  print("You can see trends for the following parameters: sleep, hydration, nutrition, stress, fatigue, soreness or overall.")
  params = raw_input('Please input params separated by a comma: ')

  paramList = [p.strip() for p in params.split(',')]
  for param in paramList:
    graphParams[param] = 'true'
  
  # individualParamTrend(graphParams)




def requestIndividualFormScore():
  ## Data needs to be organized and parsed 
  parseDataFromCSV('Individual_performance_log_data.csv')

  # process data for formscore
  individualFormScore = {
    "dates": [],
    "values": []
  }

  # get all dates for all params
  for param, data in individualPerformanceLogData.items():
    for date in data["dates"]:
      if date not in individualFormScore["dates"]:
        individualFormScore["dates"].append(date)
  
  for date in individualFormScore["dates"]:
    formscore_value = 0
    for param, data in individualPerformanceLogData.items():
      date_idx = data["dates"].index(date)
      if date_idx >= 0:
        formscore_value += data["values"][date_idx]
    individualFormScore["values"].append(formscore_value)

  # print individualFormScore
  athleteFormScore(individualFormScore)




## Currently this only shows data for one user
## TODO: allow file input to show other users
def selectKPI():
  print("Available KPIs to view: ")
  print(" (A) Athlete Param History")
  print(" (B) Athlete Form Score")

  KPI = raw_input("Please select one from the list above: ")

  ## Option A: showing individual param trend history over time
  if ((KPI == 'A') or (KPI == '(A)') or (KPI == 'a')):
    requestIndividualParamTrend()
  ## Option B: showing the total form score for one athlete over time
  elif ((KPI == 'B') or (KPI == '(B)') or (KPI == 'b')):
    requestIndividualFormScore()


################
#  START HERE  #
################

# selectKPI()






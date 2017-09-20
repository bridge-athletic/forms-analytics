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


#### FUNCTION: takes a csv file with performance log data for one user 
def loadData_oneUser(filename):

  ## empty dictionary to be filled with performance log data
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

  return individualPerformanceLogData


#### FUNCTION: takes list of params to be graphed
def requestIndividualParamTrend(individualData, params):

  #### initialize all to false
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

  paramList = [p.strip() for p in params.split(',')]
  for param in paramList:
    graphParams[param] = 'true'
  
  #### Send params to the function that graphs them in timeseries
  individualParamTrend(individualData, graphParams)


#### FUNCTION: takes params and plots on graph (timeseries)
def individualParamTrend(individualData, params):
  ## initialize the plot
  fig, ax = plt.subplots()
  graphTitle = "Individual (userId 4349) Trends for "

  ## add all params indicated by user
  ## each block adds a new plot to the figure
  if (params['fatigue'] == 'true'):
    dates = individualData["fatigue"]["dates"]
    values = individualData["fatigue"]["values"]
    ax.plot(dates, values, label='fatigue')
    graphTitle += 'Fatigue '

  if (params['soreness'] == 'true'):
    dates = individualData["soreness"]["dates"]
    values = individualData["soreness"]["values"]      
    ax.plot(dates, values, label='soreness')
    graphTitle += 'Soreness '

  if (params['stress'] == 'true'):
    dates = individualData["stress"]["dates"]
    values = individualData["stress"]["values"] 
    ax.plot(dates, values, label='stress')
    graphTitle += 'Stress '

  if (params['sleep'] == 'true'):
    dates = individualData["sleep"]["dates"]
    values = individualData["sleep"]["values"] 
    ax.plot(dates, values, label='sleep')
    graphTitle += 'Sleep '

  if (params['hydration'] == 'true'):
    dates = individualData["hydration"]["dates"]
    values = individualData["hydration"]["values"] 
    ax.plot(dates, values, label='hydration')
    graphTitle += 'Hydration '

  if (params['nutrition'] == 'true'):
    dates = individualData["nutrition"]["dates"]
    values = individualData["nutrition"]["values"] 
    ax.plot(dates, values, label='nutrition')
    graphTitle += 'Nutrition '

  if (params['overall'] == 'true'):
    dates = individualData["overall"]["dates"]
    values = individualData["overall"]["values"] 
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


#### FUNCTION: takes in processed data to calculate the form scores (sum of all responses / out of 35)
def requestIndividualFormScore(processedData):
  # process data for formscore
  individualFormScore = {
    "dates": [],
    "values": []
  }

  # get all dates for all params
  for param, data in processedData.items():
    for date in data["dates"]:
      if date not in individualFormScore["dates"]:
        individualFormScore["dates"].append(date)
  
  for date in individualFormScore["dates"]:
    formscore_value = 0
    for param, data in processedData.items():
      date_idx = data["dates"].index(date)
      if date_idx >= 0:
        formscore_value += data["values"][date_idx]
    individualFormScore["values"].append(formscore_value)

  #### Send data to function that shows timeseries of athlete's form score
  athleteFormScore(individualFormScore)

#### FUNCTION: takes the form score data and plots it on a graph (timeseries)
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
  




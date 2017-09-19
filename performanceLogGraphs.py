# Shows the trends for one athlete: sleep, hydration, nutrition, stress, fatigue, soreness, overall over time
# Can configure the trends that show based on the input

# SELECT userId, parameterId, UNIX_TIMESTAMP(recordedAt), intValue 
# FROM userparameter 
# WHERE userId in (4349) 
# AND formquestionid in (103, 104, 105, 106, 107, 108, 109) 
# LIMIT 100000;

#  492 = fatigue
#  493 = soreness
#  494 = stress
#  495 = sleep
#  496 = nutrition
#  497 = hydration
#  498 = overall

# "userid" : {
#   "param1": {
#     "dates": []
#     "values": []
#   }
# }


import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# paramIdMap = {
#   "492": "fatigue",
#   "493": "soreness",
#   "494": "stress",
#   "495": "sleep",
#   "496": "nutrition",
#   "497": "hydration",
#   "498": "overall"
# }

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
      date = datetime.date.fromtimestamp(int(row[2]))
      
      if (int(row[1]) == 492):
        individualPerformanceLogData["fatigue"]["dates"].append(date)
        individualPerformanceLogData["fatigue"]["values"].append(int(row[3]))
      if (int(row[1]) == 493):
        individualPerformanceLogData["soreness"]["dates"].append(date)
        individualPerformanceLogData["soreness"]["values"].append(int(row[3]))
      if (int(row[1]) == 494):
        individualPerformanceLogData["stress"]["dates"].append(date)
        individualPerformanceLogData["stress"]["values"].append(int(row[3]))
      if (int(row[1]) == 495):
        individualPerformanceLogData["sleep"]["dates"].append(date)
        individualPerformanceLogData["sleep"]["values"].append(int(row[3]))
      if (int(row[1]) == 496):
        individualPerformanceLogData["nutrition"]["dates"].append(date)
        individualPerformanceLogData["nutrition"]["values"].append(int(row[3]))
      if (int(row[1]) == 497):
        individualPerformanceLogData["hydration"]["dates"].append(date)
        individualPerformanceLogData["hydration"]["values"].append(int(row[3]))
      if (int(row[1]) == 498):
        individualPerformanceLogData["overall"]["dates"].append(date)
        individualPerformanceLogData["overall"]["values"].append(int(row[3]))


def timeseries(data, params, subject):

  # initialize the plot
  fig, ax = plt.subplots()

  # if (params['formscore'] == 'true'):
  #   graphTitle = "Individual (userId 4349) Form Score"
  #   values = data.iloc[[7]]

  #   ax.plot(dates, values, label='Form Score')

  #   ax.grid(True)
  #   ax.set_ylim(0, 38)
  #   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  #   fig.autofmt_xdate()
  #   ax.legend(loc=3)

  #   ## set axes and title
  #   ax.set_xlabel('Dates')
  #   ax.set_ylabel('Form Score (total)')
  #   ax.set_title(graphTitle)
  
  
  graphTitle = "Individual (userId 4349) Trends for "

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

  # add slepe trend
  if (params['sleep'] == 'true'):
    dates = individualPerformanceLogData["sleep"]["dates"]
    values = individualPerformanceLogData["sleep"]["values"] 
    ax.plot(dates, values, label='sleep')
    graphTitle += 'Sleep '

  # add slepe trend
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
  ax.set_ylim(0, 5.5)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Values')
  ax.set_title(graphTitle)
  
  plt.show()


def graphRequest(trend, graphSubject):

  form_data = parseDataFromCSV('Individual_performance_log_data.csv')

  # initialize all to false
  params = ''
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

  if (trend == 'param history'):
    print
    print("You can see trends for the following parameters: sleep, hydration, nutrition, stress, fatigue, soreness or overall.")
    params = raw_input('Please input params separated by a comma: ')

    paramList = [p.strip() for p in params.split(',')]
    
    for param in paramList:
      graphParams[param] = 'true'
    
  elif (trend == 'form score'):
    graphParams.formscore = 'true'
  
  timeseries(form_data, graphParams, graphSubject)


def selectKPI():
  print("Available KPIs to view: ")
  print(" (A) Athlete Param History")
  print(" (B) Athlete Form Score")
  # print(" (C) Team Param History")
  # print(" (D) Team Form Score")
  KPI = raw_input("Please select one from the list above: ")

  if ((KPI == 'A') or (KPI == '(A)') or (KPI == 'a')):
    graphRequest('param history', 'individual')
  elif ((KPI == 'B') or (KPI == '(B)') or (KPI == 'b')):
    graphRequest('form score', 'individual')
  # elif ((KPI == 'C') or (KPI == '(C)') or (KPI == 'c')):
  #   complianceRequest('param history', 'team')
  # elif ((KPI == 'D') or (KPI == '(D)') or (KPI == 'd')):
  #   complianceRequest('form score', 'team')



selectKPI()





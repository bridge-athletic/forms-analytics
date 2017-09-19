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

import csv
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dates = []
params = [492, 493, 494, 495, 496, 497, 498]  ## this doesn't change

# takes a file with performance log data for one user 
def parseDataFromCSV(filename):

  fatigue_data = {}
  soreness_data = {}
  stress_data = {}
  sleep_data = {}
  nutrition_data = {}
  hydration_data = {}
  overall_data = {}
  formscore_data = {}

  with open(filename) as performanceLogData:
    csvReader = csv.reader(performanceLogData)
    for row in csvReader:
      date = datetime.date.fromtimestamp(int(row[2]))
      if (date not in dates): 
        dates.append(date)
      
      if (int(row[1]) == 492):
        if (date in fatigue_data.keys()):
          fatigue_data[date].append(int(row[3]))
        else:
          fatigue_data[date] = [int(row[3])]
      if (int(row[1]) == 493):
        if (date in soreness_data.keys()):
          soreness_data[date].append(int(row[3]))
        else:
          soreness_data[date] = [int(row[3])]
      if (int(row[1]) == 494):
        if (date in stress_data.keys()):
          stress_data[date].append(int(row[3]))
        else:
          stress_data[date] = [int(row[3])]
      if (int(row[1]) == 495):
        if (date in sleep_data.keys()):
          sleep_data[date].append(int(row[3]))
        else:
          sleep_data[date] = [int(row[3])]
      if (int(row[1]) == 496):
        if (date in nutrition_data.keys()):
          nutrition_data[date].append(int(row[3]))
        else:
          nutrition_data[date] = [int(row[3])]
      if (int(row[1]) == 497):
        if (date in hydration_data.keys()):
          hydration_data[date].append(int(row[3]))
        else:
          hydration_data[date] = [int(row[3])]
      if (int(row[1]) == 498):
        if (date in overall_data.keys()):
          overall_data[date].append(int(row[3]))
        else:
          overall_data[date] = [int(row[3])]

  # oneUserData = pd.DataFrame(index=params, columns=dates)

  for date in dates:
    date_idx = int(dates.index(date))
    formscore = 0
    if (len(fatigue_data[date]) > 1):
      fatigue_data[date] = np.average(fatigue_data[date])
      formscore += fatigue_data[date]
    if (len(soreness_data[date]) > 1):
      soreness_data[date] = np.average(soreness_data[date])
      formscore += soreness_data[date]
    if (len(stress_data[date]) > 1):
      stress_data[date] = np.average(stress_data[date])
      formscore += stress_data[date]
    if (len(sleep_data[date]) > 1):
      sleep_data[date] = np.average(sleep_data[date])
      formscore += sleep_data[date]
    if (len(nutrition_data[date]) > 1):
      nutrition_data[date] = np.average(nutrition_data[date])
      formscore += nutrition_data[date]
    if (len(hydration_data[date]) > 1):
      hydration_data[date] = np.average(hydration_data[date])
      formscore += hydration_data[date]
    if (len(overall_data[date]) > 1):
      overall_data[date] = np.average(overall_data[date])
      formscore += overall_data[date]
    formscore_data[date] = formscore
    
  oneUserData = pd.DataFrame([fatigue_data, soreness_data, stress_data, sleep_data, nutrition_data, hydration_data, overall_data, formscore_data])
  return oneUserData

def timeseries(data, params, subject):

  # print data
  print data.loc[0]
  print len(dates)

  # initialize the plot
  fig, ax = plt.subplots()
  graphTitle = ''

  if (params['formscore'] == 'true'):
    graphTitle = "Individual (userId 4349) Form Score"
    values = data.iloc[[7]]

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
  
  else:
    graphTitle = "Individual (userId 4349) Trends for "

    if (params['fatigue'] == 'true'):
      values = data.iloc[[0]]
      ax.plot(dates, values, label='fatigue')
      graphTitle += 'Fatigue '

    if (params['soreness'] == 'true'):
      values = data.iloc[[1]]
      ax.plot(dates, values, label='soreness')
      graphTitle += 'Soreness '

    if (params['stress'] == 'true'):
      values = data.iloc[[2]]
      ax.plot(dates, values, label='stress')
      graphTitle += 'Stress '

    # add slepe trend
    if (params['sleep'] == 'true'):
      values = data.iloc[[3]]
      ax.plot(dates, values, label='sleep')
      graphTitle += 'Sleep '

    # add slepe trend
    if (params['hydration'] == 'true'):
      values = data.iloc[[4]]
      ax.plot(dates, values, label='hydration')
      graphTitle += 'Hydration '
    
    if (params['nutrition'] == 'true'):
      values = data.iloc[[5]]
      ax.plot(dates, values, label='nutrition')
      graphTitle += 'Nutrition '
    
    if (params['overall'] == 'true'):
      values = data.iloc[[6]]
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






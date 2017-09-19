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

oneUserData = []
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

  # print dates
  for date in dates:
    date_idx = int(dates.index(date))
    formscore = 0

    
    # fill fatigue data
    if (date not in fatigue_data.keys()):
      oneUserData[0][date_idx] = -1
    elif (len(fatigue_data[date]) > 1):
      oneUserData[0][date_idx] = np.average(fatigue_data[date])
      formscore += np.average(fatigue_data[date])
    else:
      oneUserData[0][date_idx].append(fatigue_data[0])
      formscore += fatigue_data[0]

    # fill soreness data
    if (date not in soreness_data.keys()):
      oneUserData[1][date_idx] = -1
    elif (len(soreness_data[date]) > 1):
      oneUserData[1][date_idx] = np.average(soreness_data[date])
      formscore += np.average(soreness_data[date])
    else:
      oneUserData[1][date_idx] = soreness_data[0]
      formscore += soreness_data[0]

    # fill stress data
    if (date not in stress_data.keys()):
      oneUserData[2][date_idx] = -1
    elif (len(stress_data[date]) > 1):
      oneUserData[2][date_idx] = np.average(stress_data[date])
      formscore += np.average(stress_data[date])
    else:
      oneUserData[2][date_idx] = stress_data[0]
      formscore += stress_data[0]

    # fill sleep data
    if (date not in sleep_data.keys()):
      oneUserData[3][date_idx] = -1
    elif (len(sleep_data[date]) > 1):
      oneUserData[3][date_idx] = np.average(sleep_data[date])
      formscore += np.average(sleep_data[date])
    else:
      oneUserData[3][date_idx] = sleep_data[0]
      formscore += sleep_data[0]

    # fill nutrition data
    if (date not in nutrition_data.keys()):
      oneUserData[4][date_idx] = -1
    elif (len(nutrition_data[date]) > 1):
      oneUserData[4][date_idx] = np.average(nutrition_data[date])
      formscore += np.average(nutrition_data[date])
    else:
      oneUserData[4][date_idx] = nutrition_data[0]
      formscore += nutrition_data[0]

    # fill hydration data
    if (date not in hydration_data.keys()):
      oneUserData[5][date_idx] = -1
    elif (len(hydration_data[date]) > 1):
      oneUserData[5][date_idx] = np.average(hydration_data[date])
      formscore += np.average(hydration_data[date])
    else:
      oneUserData[5][date_idx] = hydration_data[0]
      formscore += hydration_data[0]

    # fill overall data
    if (date not in overall_data.keys()):
      oneUserData[6][date_idx] = -1
    elif (len(overall_data[date]) > 1):
      oneUserData[6][date_idx] = np.average(overall_data[date])
      formscore += np.average(overall_data[date])
    else:
      oneUserData[6][date_idx] = overall_data[0]
      formscore += overall_data[0]

    # fill form score data
    oneUserData[7][date_idx] = formscore




def timeseries(params, subject):


  # initialize the plot
  fig, ax = plt.subplots()
  graphTitle = ''

  if (params['formscore'] == 'true'):
    graphTitle = "Individual (userId 4349) Form Score"
    values = []
    for value in oneUserData[7]:
      values.append(value)

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

    # add slepe trend
    if (params['sleep'] == 'true'):
      values = []
      for value in oneUserData[3]:
        values.append(value)
      ax.plot(dates, values, label='sleep')
      graphTitle += 'Sleep '

    # add slepe trend
    if (params['hydration'] == 'true'):
      values = []
      for value in oneUserData[5]:
        values.append(value)
      ax.plot(dates, values, label='hydration')
      graphTitle += 'Hydration '
    
    if (params['nutrition'] == 'true'):
      values = []
      for value in oneUserData[4]:
        values.append(value)
      ax.plot(dates, values, label='nutrition')
      graphTitle += 'Nutrition '
    
    if (params['stress'] == 'true'):
      values = []
      for value in oneUserData[2]:
        values.append(value)
      ax.plot(dates, values, label='stress')
      graphTitle += 'Stress '
    
    if (params['fatigue'] == 'true'):
      values = []
      for value in oneUserData[0]:
        values.append(value)
      ax.plot(dates, values, label='fatigue')
      graphTitle += 'Fatigue '
    
    if (params['soreness'] == 'true'):
      values = []
      for value in oneUserData[1]:
        values.append(value)
      ax.plot(dates, values, label='soreness')
      graphTitle += 'Soreness '
    
    if (params['overall'] == 'true'):
      values = []
      for value in oneUserData[6]:
        values.append(value)
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

  # # parse the file with team data
  # if (graphSubject == 'team'):
  #   parseDataFromCSV('Group_performance_log_data.csv')

  # parse the file with individual data
  if (graphSubject == 'individual'):
    parseDataFromCSV('Individual_performance_log_data.csv')

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
  
  timeseries(graphParams, graphSubject)


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






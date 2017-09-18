# Shows the trends for one athlete: sleep, hydration, nutrition, stress, fatigue, soreness, overall over time
# Can configure the trends that show based on the input

# SELECT userId, parameterId, UNIX_TIMESTAMP(recordedAt), intValue 
# FROM userparameter 
# WHERE userId in (4349) 
# AND formquestionid in (103, 104, 105, 106, 107, 108, 109) 
# LIMIT 100000;

import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# initialize each set of data 
sleepDates = []
sleepValues = []
sorenessDates = []
sorenessValues =[]
fatigueDates = []
fatigueValues =[]
stressDates = []
stressValues =[]
nutritionDates = []
nutritionValues =[]
hydrationDates = []
hydrationValues =[]
overallDates = []
overallValues =[]
formScoreDates = []
formScoreValues = []

# takes a file with performance log data from one user and 
# parses the data into arrays so it can be plotted
def parseDataFromFile(filename):
# def parseDataFromFile(filename, daterange):

  # start_date = None
  # if (daterange = 30):
  #   start_date = datetime.datetime.now() + datetime.timedelta(-30)
  #   print start_date
  # if (daterange = 30):
  #   start_date = datetime.datetime.now() + datetime.timedelta(-30)
  #   print start_date


  # fill the empty lists from above
  with open(filename) as performanceLogData:
    csvReader = csv.reader(performanceLogData)
    for row in csvReader:
      date = datetime.date.fromtimestamp(int(row[2]))

      # TODO: make one function and pass in the parameterId and two lists
      if (int(row[1]) == 492):  # parameter = fatigue
        if (date in fatigueDates):
          # if date already in the list, average the values
          idx = fatigueDates.index(date)
          fatigueValues[idx] = (fatigueValues[idx] + int(row[3]))/2
        else:
          # otherwise add the date and value to the lists
          fatigueDates.append(date)
          fatigueValues.append(int(row[3]))
      
      elif (int(row[1]) == 493):  # parameter = soreness
        if (date in sorenessDates):
          # if date already in the list, average the values
          idx = sorenessDates.index(date)
          sorenessValues[idx] = (sorenessValues[idx] + int(row[3]))/2
        else:
          # otherwise add the date and value to the lists
          sorenessDates.append(date)
          sorenessValues.append(int(row[3]))

      elif (int(row[1]) == 494):
      # parameter = stress
        if (date in stressDates):
          # if date already in the list, average the values
          idx = stressDates.index(date)
          stressValues[idx] = (stressValues[idx] + int(row[3]))/2
        else:
          # otherwise add the date and value to the lists
          stressDates.append(date)
          stressValues.append(int(row[3]))

      elif (int(row[1]) == 495):
      # parameter = sleep
        if (date in sleepDates):
          # if date already in the list, average the values
          idx = sleepDates.index(date)
          sleepValues[idx] = (sleepValues[idx] + int(row[3]))/2
        else:
          # otherwise add the date and value to the lists
          sleepDates.append(date)
          sleepValues.append(int(row[3]))

      elif (int(row[1]) == 496):
      # parameter = nutrition
        if (date in nutritionDates):
          # if date already in the list, average the values
          idx = nutritionDates.index(date)
          nutritionValues[idx] = (nutritionValues[idx] + int(row[3]))/2
        else:
          # otherwise add the date and value to the lists
          nutritionDates.append(date)
          nutritionValues.append(int(row[3]))

      elif (int(row[1]) == 497):
      # parameter = hydration
        if (date in hydrationDates):
          # if date already in the list, average the values
          idx = hydrationDates.index(date)
          hydrationValues[idx] = (hydrationValues[idx] + int(row[3]))/2
        else:
          # otherwise add the date and value to the lists
          hydrationDates.append(date)
          hydrationValues.append(int(row[3]))

      elif (int(row[1]) == 498):
      # parameter = overall
        if (date in overallDates):
          # if date already in the list, average the values
          idx = overallDates.index(date)
          overallValues[idx] = (overallValues[idx] + int(row[3]))/2
        else:
          # otherwise add the date and value to the lists
          overallDates.append(date)
          overallValues.append(int(row[3]))


def timeseries(params, subject):

  # initialize the plot
  fig, ax = plt.subplots()
  graphTitle = ''
  if ((subject == 'team') or (subject == 'Team')):
    graphTitle = "Team Trend for "
  else:
    graphTitle = "Individual (userId 4349) Trends for "

  # add all requested trends
  if (params['sleep'] == 'true'):
    ax.plot(sleepDates, sleepValues, label='sleep')
    graphTitle += 'Sleep '
  if (params['hydration'] == 'true'):
    ax.plot(hydrationDates, hydrationValues, label='hydration')
    graphTitle += 'Hydration '
  if (params['nutrition'] == 'true'):
    ax.plot(nutritionDates, nutritionValues, label='nutrition')
    graphTitle += 'Nutrition '
  if (params['stress'] == 'true'):
    ax.plot(stressDates, stressValues, label='stress')
    graphTitle += 'Stress '
  if (params['fatigue'] == 'true'):
    ax.plot(fatigueDates, fatigueValues, label='fatigue')
    graphTitle += 'Fatigue '
  if (params['soreness'] == 'true'):
    ax.plot(sorenessDates, sorenessValues, label='soreness')
    graphTitle += 'Soreness '
  if (params['overall'] == 'true'):
    ax.plot(overallDates, overallValues, label='overall')
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


def graphRequest(graphSubject):
  # prompt user for the details 
  # graphSubject = raw_input('Team or individual results? ')
  # if (graphSubject not in ['team', 'Team', 'individual', 'Individual']):
  #   print ("Invalid entry, please try again.")
  #   graphSubject = raw_input('Team or individual results? ')
  print
  print
  print("You can see trends for the following parameters: sleep, hydration, nutrition, stress, fatigue, soreness, overall or the form score.")
  params = raw_input('Please input params separated by a comma: ')
  
  # print
  # print("You can see trends for the past 30 day, 90 days or all data.")
  # timeRange = raw_input('Please select 30, 90 or all')

  # dateRange = 0
  # if ((timeRange = 30) or (timeRange = 90):
  #   dateRange = timeRange

  # parse the file with team data
  if ((graphSubject == 'team') or (graphSubject == 'Team')):
    parseDataFromFile('Group_performance_log_data.csv')

  # parse the file with individual data
  if ((graphSubject == 'individual') or (graphSubject == 'Individual')):
    parseDataFromFile('Individual_performance_log_data.csv')

  paramList = [p.strip() for p in params.split(',')]
  
  # initialize all to false
  graphParams = {
    'sleep': 'false',
    'hydration': 'false',
    'nutrition': 'false',
    'stress': 'false',
    'fatigue': 'false',
    'soreness': 'false',
    'overall': 'false',
  }
  for param in paramList:
    graphParams[param] = 'true'

  timeseries(graphParams, graphSubject)

def complianceRequest(subject):
  print "working on this!"


def selectKPI():
  print("Available KPIs to view: ")
  print (" (A) Athlete Param History")
  print (" (B) Team Param History")
  print (" (C) Athlete Compliance")
  print (" (D) Team Compliance")
  KPI = raw_input("Please select one from the list above: ")

  if ((KPI == 'A') or (KPI == '(A)') or (KPI == 'a')):
    graphRequest("individual")
  elif ((KPI == 'B') or (KPI == '(B)') or (KPI == 'b')):
    graphRequest("team")
  elif ((KPI == 'C') or (KPI == '(C)') or (KPI == 'c')):
    complianceRequest("individual")
  elif ((KPI == 'D') or (KPI == '(D)') or (KPI == 'd')):
    complianceRequest("team")



selectKPI()






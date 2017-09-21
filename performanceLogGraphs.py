# SELECT userId, parameterId, UNIX_TIMESTAMP(recordedAt), intValue 
# FROM userparameter 
# WHERE userId in (4349) 
# AND formquestionid in (103, 104, 105, 106, 107, 108, 109) 
# LIMIT 100000;


### Fatigue | 492 | 1 = Good, 5 = Bad
### Soreness | 493 | 1 = Good, 5 = Bad
### Stress | 494 | 1 = Good, 5 = Bad
### Sleep | 495 | 1 = Bad, 5 = Good
### Nutrition | 496 | 1 = Bad, 5 = Good
### Hydration | 497 | 1 = Bad, 5 = Good
### Overall | 498 | 1 = Bad, 5 = Good

### Total Score | 1 = Bad, 100 = Good


import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from datetime import date, datetime, timedelta


#### FUNCTION: takes a csv file with performance log data for one user
#### NOTE: this function organizes raw data 
def loadData_oneUser(filecsv):

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

  with open(filecsv) as performanceLogData:
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


#### FUNCTION: takes a csv file with performance log data for one user 
#### NOTE: this function organizes question scores
def loadScores_oneUser(filecsv):

  ## empty dictionary to be filled with performance log data
  individualPerformanceLogScores = {
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

  with open(filecsv) as performanceLogData:
    csvReader = csv.reader(performanceLogData)

    for row in csvReader:
      ## convert date to YYYY-MM-DD
      date = datetime.date.fromtimestamp(int(row[2]))
      
      ## fatigue data; parameterId 492
      if (int(row[1]) == 492):
        individualPerformanceLogData["fatigue"]["dates"].append(date)
        ## calculate score for fatigue
        score = ((5 - int(row[3])) + 1)
        individualPerformanceLogData["fatigue"]["values"].append(score)
      
      ## soreness data; parameterId 493
      if (int(row[1]) == 493):
        individualPerformanceLogData["soreness"]["dates"].append(date)
        ## calculate score for soreness
        score = ((5 - int(row[3])) + 1)
        individualPerformanceLogData["soreness"]["values"].append(score)
      
      ## stress data; parameterId 494
      if (int(row[1]) == 494):
        individualPerformanceLogData["stress"]["dates"].append(date)
        ## calculate score for sleep
        score = ((5 - int(row[3])) + 1)
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


#### FUNCTION: processes data with means, uses the loadData function
def dataPostMeanProcessing_oneUser(filecsv):
  # rawData = loadData_oneUser(filecsv)
  rawData= loadScores_oneUser(filecsv)
  dataPostProcessing = {}

  for param, data in rawData.items():
    datesRaw = rawData[param]['dates']
    valuesRaw = rawData[param]['values']

    datesUniqueSet = sorted(list(set(datesRaw)))

    # Initializing lists to store unique dates and the corresponding values, using max or min filetering.
    datesUnique = []
    # valuesUniqueMax = []
    valuesUniqueMean = []

    for i, date in enumerate(datesUniqueSet):
      # Initialize tempValues
      tempValues = []
      # Find all values corresponding to the date
      tempValues = [valuesRaw[j] for j, x in enumerate(datesRaw) if x == date]

      # If data exists (which it)
      if(len(tempValues)>0):

        # Store unique date
        datesUnique.append(date)
        # Store mean of values
        valuesUniqueMean.append(sum(tempValues)/float(len(tempValues)))

    # Add the unique lists to the main data structure
    dataPostProcessing[param] = {
      "dates": [],
      "values": []
    }
    dataPostProcessing[param]["dates"] = datesUnique
    dataPostProcessing[param]["values"] = valuesUniqueMean

  return dataPostProcessing


#### FUNCTION: calculates form score, uses the dataPostMeanProcessing function
def dataWithFormScore(filecsv):
  processedData = dataPostMeanProcessing_oneUser(filecsv)
  processedData["total"] = {
    "dates": [],
    "values": []
  }

  allDates = []
  # build array with all dates from each param list
  for param, data in processedData.items():
    allDates += data['dates']

  uniqueAllDates = sorted(list(set(allDates)))
  for uniqueDate in uniqueAllDates:
    # Initialize to hold the values for each date
    sumValue = 0
    numParams = 0
    
    for param, data in processedData.items():

      if uniqueDate in data["dates"]:
        idx = data["dates"].index(uniqueDate)
        sumValue += data["values"][idx]
        numParams += 1

    processedData["total"]["dates"].append(uniqueDate)
    maxPts = numParams*5
    processedData["total"]["values"].append((sumValue*100)/maxPts)

  return processedData


#### FUNCTION: calculates 7 pt moving average
def dataPointMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)

  individualAvgData = {}

  for param, data in processedData.items():
    ## Start at 7th spot since creating a 7 point moving average
    idx = 7

    ## Initialize temp lists to hold data as we calculate it
    dates = []
    movingAvg = []
    
    ## Get averages for each day until reach the last date in list
    while idx < len(data["dates"]):
      ## Store date of moving average below
      dates.append(data["dates"][idx])
      
      ## Average past 7 days and store in temp list
      mvgAvg = (sum(data["values"][idx-7:idx]))/7
      # print mvgAvg
      movingAvg.append(mvgAvg)
      
      ## Next day
      idx += 1

    # print len(dates)
    # print len(movingAvg)

    # print dates
    # print movingAvg

    individualAvgData[param] = {
      "dates": dates,
      "averages": movingAvg
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 7 day moving average
def dataDayMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)

  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]
  # print startDate
  # print endDate

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  
  ## Go through each param 
  for param, data in processedData.items():
    ## Start at 7th spot for 7 day moving average
    idx = 7

    ## Initialize temp list to hold data as we calculate it
    movingAvg = []

    ## Go though all dates between the first and last
    for date in allDates:      
      mygAvg = 0
      ## Check if date in date list, if yes: use data, if no: use value from day before
      if date in data["dates"]:
        ## Average past 7 days and store in temp list
        mvgAvg = (sum(data["values"][idx-7:idx]))/7
      else:
        ## Take the last value from the list (previous day's average)
        mvgAvg = movingAvg[-1]

      ## Store latest moving average in list
      movingAvg.append(mvgAvg)

      ## Go to next date in the allDates list
      idx += 1


    individualAvgData[param] = {
      "dates": dates,
      "averages": movingAvg
    }




  # need to get first and last date in combined list
  # make new list of ALL dates between first and last 
  # go through each date in list, if data, add it, if not, take the one before 
  # go until the end


#### FUNCTION: takes moving average data and plots it with the form score
def showMovingAverageAndTotalScore(filecsv, parameter):

  avgData, processedData = dataPointMovingAverage(filecsv)

  ## initialize the plot
  fig, ax = plt.subplots()
  graphTitle = "Individual 7 Point Moving Average for "

  if (parameter == 'fatigue'):
    ## update data so its out of 100
    values = [((v*100)/5) for v in avgData["fatigue"]["averages"]]
    dates = avgData["fatigue"]["dates"]
    ax.plot(dates, values, label='fatigue')
    graphTitle += 'Fatigue '

  elif (parameter == 'soreness'):
    dates = individualData["soreness"]["dates"]
    values = [((v*100)/5) for v in avgData["soreness"]["averages"]]
    ax.plot(dates, values, label='soreness')
    graphTitle += 'Soreness '

  elif (parameter == 'stress'):
    dates = individualData["stress"]["dates"]
    values = [((v*100)/5) for v in avgData["stress"]["averages"]]
    ax.plot(dates, values, label='stress')
    graphTitle += 'Stress '

  elif (parameter == 'sleep'):
    dates = individualData["sleep"]["dates"]
    values = [((v*100)/5) for v in avgData["sleep"]["averages"]]
    ax.plot(dates, values, label='sleep')
    graphTitle += 'Sleep '

  elif (parameter == 'hydration'):
    dates = individualData["hydration"]["dates"]
    values = [((v*100)/5) for v in avgData["hydration"]["averages"]]
    ax.plot(dates, values, label='hydration')
    graphTitle += 'Hydration '

  elif (parameter == 'nutrition'):
    dates = individualData["nutrition"]["dates"]
    values = [((v*100)/5) for v in avgData["nutrition"]["averages"]]
    ax.plot(dates, values, label='nutrition')
    graphTitle += 'Nutrition '

  elif (parameter == 'overall'):
    dates = individualData["overall"]["dates"]
    values = [((v*100)/5) for v in avgData["overall"]["averages"]]
    ax.plot(dates, values, label='overall')
    graphTitle += 'Overall '

  ## Add the total form score 
  totalDates = processedData["total"]["dates"]
  totalValues = processedData["total"]["values"]
  ax.plot(totalDates, totalValues, label='Total Score')
  graphTitle += 'with Total Score '

  ax.grid(True)
  ax.set_ylim(0, 105)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Values')
  ax.set_title(graphTitle)
  
  plt.show()


#### FUNCTION: plot raw data with mean / max data to understand different 
def showRawMeanMax(filecsv):
  #### Load data from csv file 
  dataRaw = loadData_oneUser(filecsv)

  parameterName = 'overall'

  datesRaw = dataRaw[parameterName]['dates']
  valuesRaw = dataRaw[parameterName]['values']
  datesUniqueSet = sorted(list(set(datesRaw)))

  # Initializing lists to store unique dates and the corresponding values, using max or min filetering.
  datesUnique = []
  valuesUniqueMax = []
  valuesUniqueMean = []

  for i, date in enumerate(datesUniqueSet):

    # Initialize tempValues
    tempValues = []
    # Find all values corresponding to the date
    tempValues = [valuesRaw[j] for j, x in enumerate(datesRaw) if x == date]

    # print tempValues
    # If data exists (which it)
    if(len(tempValues)>0):

      # Store unique date
      datesUnique.append(date)
      # Store mean of values
      valuesUniqueMean.append(sum(tempValues)/float(len(tempValues)))
      valuesUniqueMax.append(max(tempValues))


  #### Plotting data
  fig, ax = plt.subplots()
  ax.plot(datesUnique, valuesUniqueMean, label='Unique Mean')
  ax.plot(datesUnique, valuesUniqueMax, label='Unique Max')
  ax.plot(datesRaw, valuesRaw, label='Raw Data')
  ax.grid(True)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=4)
  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel(parameterName)
  ax.set_title(parameterName)
  plt.show()


#### FUNCTION: takes params and plots on graph (timeseries)
def individualParamTrend(filecsv, parameters):
  individualData = dataPostMeanProcessing_oneUser(filecsv)

  #### initialize all to false
  params = {
    'sleep': 'false',
    'hydration': 'false',
    'nutrition': 'false',
    'stress': 'false',
    'fatigue': 'false',
    'soreness': 'false',
    'overall': 'false'
  }

  paramList = [p.strip() for p in parameters.split(',')]
  for param in paramList:
    graphParams[param] = 'true'

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


#### FUNCTION: plots form score data on a graph (timeseries)
def graphFormScore(filecsv, userId):

  dataFormScore = dataWithFormScore(filecsv)
  dates = dataFormScore["total"]["dates"]
  values = dataFormScore["total"]["values"]

  fig, ax = plt.subplots()
  graphTitle = "Individual (userId " + userId +") Form Score"
  dates = data["dates"]
  values = data["values"]
  ax.plot(dates, values, label='Form Score')

  ax.grid(True)
  ax.set_ylim(0, 100)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Form Score (total)')
  ax.set_title(graphTitle)

  plt.show()
  

#### FUNCTION: plots parameter with formscore 
def graphParamAndFormScore(filecsv, parameter):
  individualData = dataWithFormScore(filecsv)

  ## initialize the plot
  fig, ax = plt.subplots()
  graphTitle = "Individual Trends for "

  if (parameter == 'fatigue'):
    ## update data so its out of 100
    values = [((v*100)/5) for v in individualData["fatigue"]["values"]]
    dates = individualData["fatigue"]["dates"]
    ax.plot(dates, values, label='fatigue')
    graphTitle += 'Fatigue '

  elif (parameter == 'soreness'):
    dates = individualData["soreness"]["dates"]
    values = [((v*100)/5) for v in individualData["soreness"]["values"]]
    ax.plot(dates, values, label='soreness')
    graphTitle += 'Soreness '

  elif (parameter == 'stress'):
    dates = individualData["stress"]["dates"]
    values = [((v*100)/5) for v in individualData["stress"]["values"]]
    ax.plot(dates, values, label='stress')
    graphTitle += 'Stress '

  elif (parameter == 'sleep'):
    dates = individualData["sleep"]["dates"]
    values = [((v*100)/5) for v in individualData["sleep"]["values"]]
    ax.plot(dates, values, label='sleep')
    graphTitle += 'Sleep '

  elif (parameter == 'hydration'):
    dates = individualData["hydration"]["dates"]
    values = [((v*100)/5) for v in individualData["hydration"]["values"]]
    ax.plot(dates, values, label='hydration')
    graphTitle += 'Hydration '

  elif (parameter == 'nutrition'):
    dates = individualData["nutrition"]["dates"]
    values = [((v*100)/5) for v in individualData["nutrition"]["values"]]
    ax.plot(dates, values, label='nutrition')
    graphTitle += 'Nutrition '

  elif (parameter == 'overall'):
    dates = individualData["overall"]["dates"]
    values = [((v*100)/5) for v in individualData["overall"]["values"]]
    ax.plot(dates, values, label='overall')
    graphTitle += 'Overall '

  ## Add the total form score 
  totalDates = individualData["total"]["dates"]
  totalValues = individualData["total"]["values"]
  ax.plot(totalDates, totalValues, label='Total Score')
  graphTitle += 'with Total Score '

  ax.grid(True)
  ax.set_ylim(0, 105)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Values')
  ax.set_title(graphTitle)
  
  plt.show()
















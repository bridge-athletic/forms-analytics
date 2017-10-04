# SELECT userId, parameterId, UNIX_TIMESTAMP(recordedAt), intValue 
# FROM userparameter 
# WHERE userId in (4349) 
# AND formquestionid in (103, 104, 105, 106, 107, 108, 109) 
# LIMIT 100000;


### Fatigue | 492 | 1 = Good, 5 = Bad
### Soreness | 493 | 1 = Good, 5 = Bad
### Stress | 494 | 1 = Good, 5 = Bad
### SleepQuality | 495 | 1 = Bad, 5 = Good
### Nutrition | 496 | 1 = Bad, 5 = Good
### Hydration | 497 | 1 = Bad, 5 = Good
### Overall | 498 | 1 = Bad, 5 = Good

### Total Score | 1 = Bad, 100 = Good


import csv
import copy
import datetime
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.plotly as py
import plotly.figure_factory as ff
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
    "sleepQuality": {
      "dates": [],
      "values": []
    },
    "sleepQuantity": {
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
      
      ## sleepQuality data; parameterId 495
      if (int(row[1]) == 495):
        individualPerformanceLogData["sleepQuality"]["dates"].append(date)
        individualPerformanceLogData["sleepQuality"]["values"].append(int(row[3]))

      ## sleepQuantity data; parameterId 614
      if (int(row[1]) == 495):
        individualPerformanceLogData["sleepQuantity"]["dates"].append(date)
        individualPerformanceLogData["sleepQuantity"]["values"].append((int(row[3]))/1000.0)
      
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
    "sleepQuality": {
      "dates": [],
      "values": []
    },
    "sleepQuantity": {
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
        individualPerformanceLogScores["fatigue"]["dates"].append(date)
        ## calculate score for fatigue
        score = ((5 - int(row[3])) + 1)
        individualPerformanceLogScores["fatigue"]["values"].append(score)
      
      ## soreness data; parameterId 493
      if (int(row[1]) == 493):
        individualPerformanceLogScores["soreness"]["dates"].append(date)
        ## calculate score for soreness
        score = ((5 - int(row[3])) + 1)
        individualPerformanceLogScores["soreness"]["values"].append(score)
      
      ## stress data; parameterId 494
      if (int(row[1]) == 494):
        individualPerformanceLogScores["stress"]["dates"].append(date)
        ## calculate score for sleepQuality
        score = ((5 - int(row[3])) + 1)
        individualPerformanceLogScores["stress"]["values"].append(int(row[3]))
      
      ## sleepQuality data; parameterId 495
      if (int(row[1]) == 495):
        individualPerformanceLogScores["sleepQuality"]["dates"].append(date)
        individualPerformanceLogScores["sleepQuality"]["values"].append(int(row[3]))
      
      ## sleepQuantity data; parameterId 614
      if (int(row[1]) == 614):
        individualPerformanceLogScores["sleepQuantity"]["dates"].append(date)
        individualPerformanceLogScores["sleepQuantity"]["values"].append((int(row[3]))/1000.0)

      ## nutrition data; parameterId 496
      if (int(row[1]) == 496):
        individualPerformanceLogScores["nutrition"]["dates"].append(date)
        individualPerformanceLogScores["nutrition"]["values"].append(int(row[3]))
      
      ## hydration data; parameterId 497
      if (int(row[1]) == 497):
        individualPerformanceLogScores["hydration"]["dates"].append(date)
        individualPerformanceLogScores["hydration"]["values"].append(int(row[3]))
      
      ## overall data; parameterId 498
      if (int(row[1]) == 498):
        individualPerformanceLogScores["overall"]["dates"].append(date)
        individualPerformanceLogScores["overall"]["values"].append(int(row[3]))

  return individualPerformanceLogScores


#### FUNCTION: processes data with means, uses the loadData function
#### CURRENTLY: using form score data object
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


#### FUNCTION: calculates form score, does NOT include the hours of sleep
#### uses the dataPostMeanProcessing function
def dataWithFormScore(filecsv):
  processedData = dataPostMeanProcessing_oneUser(filecsv)
  processedData["total"] = {
    "dates": [],
    "values": []
  }

  allDates = []
  # build array with all dates from each param list
  for param, data in processedData.items():
    if param != "sleepQuantity":
      allDates += data['dates']

  uniqueAllDates = sorted(list(set(allDates)))
  for uniqueDate in uniqueAllDates:
    # Initialize to hold the values for each date
    sumValue = 0
    numParams = 0
    
    for param, data in processedData.items():
      ## Don't include hours of sleep
      if param != "sleepQuantity":
        if uniqueDate in data["dates"]:
          idx = data["dates"].index(uniqueDate)
          sumValue += data["values"][idx]
          numParams += 1

    processedData["total"]["dates"].append(uniqueDate)
    maxPts = numParams*5
    processedData["total"]["values"].append((sumValue*100)/maxPts)

  return processedData


#### FUNCTION: calculates and shows number of questions answered for each form submission
def questionsAnsweredPerSubmission(filecsv):
  # go through all dates from total score
  # add one if the date exists in each parameter

  processedData = dataWithFormScore(filecsv)

  ## Already went through and got all dates that have one or more response recorded
  dates = processedData["total"]["dates"]
  numResponses = []

  for date in dates:
    answers = 0
    for param, data in processedData.items(): 
      if param != "total":
        if date in data["dates"]:
          answers += 1

    numResponses.append(answers)

  fig, ax = plt.subplots()
  graphTitle = "Number of Questions Answered per Form Submission (max. 8)"
  ax.plot(dates, numResponses, label='Num. Questions Answered')

  ax.grid(True)
  ax.set_ylim(0, 8.5)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Num. Questions Answered')
  ax.set_title(graphTitle)

  plt.savefig("Responses_per_submission.png")
  plt.show()


#### FUNCTION: calculates 7 PT moving average
def sevenPointMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)
  
  individualAvgData = {}

  for param, data in processedData.items():

    ## Initializing list to convolve with question scores
    n = [1,1,1,1,1,1,1]

    ## Get moving sum
    preAverages = np.convolve(data["values"], n, mode='valid')

    ## Divide all items by 7 to get moving average
    averages = [x/7 for x in preAverages]

    ## Additional calculations needed if switch convolve mode to full
    # averages = [x/(n+1) if n+1 < 7 else x/7 for n, x in enumerate(preAverages)]

    individualAvgData[param] = {
      ## Remove the first 6 dates since we are using convolve mode = valid
      "dates": data["dates"][6:],
      "averages": averages
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 7 PT EXPONENTIAL moving average
def sevenPointExponentialMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)
  
  individualAvgData = {}

  for param, data in processedData.items():

    ## Initializing list to convolve with question scores
    ## the np.convolve function will invert this list
    n = [1,0.5,0.25,0.125,0.0625,0.03125,0.015625]

    ## Get moving sum
    preAverages = np.convolve(data["values"], n, mode='valid')

    ## Divide all items by 7 to get moving average
    averages = [x/(sum(n)) for x in preAverages]

    individualAvgData[param] = {
      ## Remove the first 6 dates since we are using convolve mode = valid
      "dates": data["dates"][6:],
      "averages": averages
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 7 PT WEIGHTED moving average in slightly different way
def sevenPointWeightedMovingAverage(filecsv):
  ## Get the simple 7 point moving average
  avgData, processedData = sevenPointMovingAverage(filecsv)

  individualAvgData = {}
 
  ## Want a 7 point moving average
  n = 7
  
  ## Get multiplier, force the float
  k = 2.0/(n+1)

  for param, data in processedData.items():
    firstMA = avgData[param]["averages"][0]
    expMA = []

    for i, d in enumerate(data["values"]):
      ## Initialize exponential moving average (ema)
      ema = 0

      ## Use the simple moving average for first data point
      if i == 0:
        ema = ((d - firstMA) * k) + firstMA

      ## Otherwise use EMA = ((Current price - Previous EMA) * k) + Previous EMA
      else:
        ema = ((d - expMA[-1]) * k) + expMA[-1]
     
      expMA.append(ema)

    individualAvgData[param] = {
      "dates": data["dates"],
      "averages": expMA
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 7 DAY moving average
def sevenDayMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)

  individualAvgData = {}

  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    allData = []

    ## Get a list of data with -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        allData.append(data["values"][idx])
      else:
        ## Put -1 as filler to filter out later
        allData.append(-1)

    n = [1,1,1,1,1,1,1]
    preAverages = np.convolve(allData, n, mode='valid')

    movingAverage = []
    ## Go through and find out what the denominator should be
    for i, x in enumerate(preAverages):

      ## Get the seven values that contributed to this data point
      tempValues = allData[i:(i+7)]

      ## Find out how many should be filtered out
      filtered = tempValues.count(-1)
      dataPoints = (7 - filtered)

      if dataPoints == 0:
        ## If there were no data points in the seven days, take the average from the previous day
        movingAverage.append(movingAverage[-1])
      else:
        
        ## Add sum / actual number of data points that contributed
        movingAverage.append((x+filtered)/dataPoints)

    individualAvgData[param] = {
      "dates": allDates[6:],
      "averages": movingAverage
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 7 DAY EXPONENTIAL // WEIGHTED moving average
def sevenDayExponentialMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    allData = []
    expMA = []

    ## Fill allData -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        allData.append(data["values"][idx])
      else:
        ## Put -1 as filler to filter out later
        allData.append(-1)


    ### Exponential
    # n = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

    ## Weighted A
    n = [0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

    ## Weighted B
    # n = [0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 7th number
    i = 6
    while i < len(allData):
      tempValues = allData[i-6:i+1]
      ema = 0.0
      dem = 0.0
      
      ## Go though list and calculate the EMA for the selected seven days
      for j, v in enumerate(tempValues):
        if v != -1:
          ema += (v * n[j])
          dem += n[j]
      
      if ema == 0:
        # expMA.append(None)
        expMA.append(expMA[-1])
      else:
        expMA.append(ema/dem)
      
      ## Go to next 7 days
      i += 1

    individualAvgData[param] = {
      "dates": allDates[6:],
      "averages": expMA
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 28 DAY WEIGHTED moving average
def twentyEightDayExponentialMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    allData = []
    expMA = []

    ## Fill allData -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        allData.append(data["values"][idx])
      else:
        ## Put -1 as filler to filter out later
        allData.append(-1)


    ### Exponential
    # n = [ 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

    ## Weighted A // 1/2, 1/3...1/14
    # n = [0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0769, 0.0833, 0.0909, 0.1, 0.1111, 0.125, 0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

    ## Weighted B // 2/2, 2/3, 2/4...2/14
    n = [0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 7th number
    i = 27
    while i < len(allData):
      tempValues = allData[i-27:i+1]
      ema = 0.0
      dem = 0.0
      
      ## Go though list and calculate the EMA for the selected seven days
      for j, v in enumerate(tempValues):
        if v != -1:
          ema += (v * n[j])
          dem += n[j]
      
      if ema == 0:
        # expMA.append(None)
        expMA.append(expMA[-1])
      else:
        expMA.append(ema/dem)
      
      ## Go to next 7 days
      i += 1

    individualAvgData[param] = {
      "dates": allDates[27:],
      "averages": expMA
    }

  return individualAvgData, processedData


#### FUNCITON: calculates the standard deviation from score data
def zScore90Days(filecsv):
  processedData = dataWithFormScore(filecsv)
  individualAvgData = {}
 
  for param, data in processedData.items():
    meanData = []
    stdData = []

    for d in data["dates"]:
      
      ## For each date, get the mean and std for the past 90 days
      ninetyDaysAgo = (d - datetime.timedelta(days = 90))
      ninetyDayData = []
      
      ## Go through dates again to find the values in past 90 days
      for j, innerDate in enumerate(data["dates"]):
        if ((innerDate < d) and (innerDate > ninetyDaysAgo)):

          ## Add the value to the temp list
          ninetyDayData.append(data["values"][j])

      meanData.append(np.mean(ninetyDayData))
      stdData.append(np.std(ninetyDayData))


    individualAvgData[param] = {
      "dates": data["dates"],
      "values": data["values"],
      "means": meanData,
      "std": stdData
    }

  # Add z-score for the 90 day avg and std
  for param, data in individualAvgData.items():
    zscoreData = []

    for i, d in enumerate(data["dates"]):

      zscore = (data["values"][i] - data["means"][i]) / data["std"][i]
      zscoreData.append(zscore)

    individualAvgData[param]["zscore90"] = zscoreData

  return individualAvgData, processedData


#### FUNCITON: calculates the standard deviation from score data
def zScoreAllData(filecsv):
  zScoreData, processedData = zScore90Days(filecsv)
  individualAvgData = {}
 
  for param, data in zScoreData.items():
    meanData = np.mean(data["values"])
    stdData = np.std(data["values"])

    data["meanAll"] = meanData
    data["stdAll"] = stdData

  # Add z-score for all data avg and std
  for param, data in zScoreData.items():
    zscoreDataTemp = []
  
    for i, d in enumerate(data["dates"]):

      zscore = (data["values"][i] - data["meanAll"]) / data["stdAll"]
      zscoreDataTemp.append(zscore)

    zScoreData[param]["zscoreAll"] = zscoreDataTemp

  return zScoreData, processedData


#### FUNCTION: calculates 7 DAY WEIGHTED moving average
def sevenDayWeightedlMovingAverage(filecsv):
  processedData = dataWithFormScore(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    allData = []
    expMA = []

    ## Fill allData -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        allData.append(data["values"][idx])
      else:
        ## Put -1 as filler to filter out later
        allData.append(-1)


    ### Exponential
    # n = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

    ## Weighted A
    # n = [0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

    ## Weighted B
    n = [0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 7th number
    i = 6
    while i < len(allData):
      tempValues = allData[i-6:i+1]
      ema = 0.0
      dem = 0.0
      
      ## Go though list and calculate the EMA for the selected seven days
      for j, v in enumerate(tempValues):
        if v != -1:
          ema += (v * n[j])
          dem += n[j]
      
      if ema == 0:
        # expMA.append(None)
        expMA.append(expMA[-1])
      else:
        expMA.append(ema/dem)
      
      ## Go to next 7 days
      i += 1

    individualAvgData[param] = {
      "dates": allDates[6:],
      "averages": expMA
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 7 DAY WEIGHTED moving average WITH Z-SCORE
def sevenDayWeightedMovingAverageWithZScore(filecsv):
  processedData, individualData = zScoreAllData(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    ## make two lists, one for the data in past 90 days and other for all data collected
    allData = []
    ninetyData = []
    
    ## Initialize arrays for the moving average for each set of data
    maAll = []
    ma90 = []

    ## Fill allData -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        allData.append(data["zscoreAll"][idx])
        ninetyData.append(data["zscore90"][idx])
      else:
        ## Put -1 as filler to filter out later
        allData.append(-1)
        ninetyData.append(-1)


    ### Exponential
    # n = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

    ## Weighted A
    # n = [0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

    ## Weighted B
    n = [0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 7th number
    i = 6
    while i < len(allData):
      tempValuesAll = allData[i-6:i+1]
      emaAll = 0.0
      demAll = 0.0
      
      ## First go though list and calculate the moving average for the selected seven days for all data
      for j, v in enumerate(tempValuesAll):
        if v != -1:
          emaAll += (v * n[j])
          demAll += n[j]
      
      if emaAll == 0:
        # maAll.append(None)
        maAll.append(maAll[-1])
      else:
        maAll.append(emaAll/demAll)
      
      tempValues90 = ninetyData[i-6:i+1]
      ema90 = 0.0
      dem90 = 0.0

      ## Then go though list and calculate the moving average for the selected seven days for the 90 day data
      for j, v in enumerate(tempValues90):
        if v != -1:
          ema90 += (v * n[j])
          dem90 += n[j]
      
      if ema90 == 0:
        # ma90.append(None)
        ma90.append(ma90[-1])
      else:
        ma90.append(ema90/dem90)
      
      ## Go to next 7 days
      i += 1

    ## Averages using the z score
    individualAvgData[param] = {
      "dates": allDates[6:],
      "averagesAll": maAll,
      "averages90": ma90
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 14 DAY WEIGHTED moving average with Z-SCORE
def fourteenDayWeightedMovingAverage(filecsv):
  processedData, individualData = zScoreAllData(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    allData = []
    expMA = []

    ## Fill allData -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        allData.append(data["zscore"][idx])
      else:
        ## Put -1 as filler to filter out later
        allData.append(-1)


    ### Exponential
    # n = [ 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

    ## Weighted A // 1/2, 1/3...1/14
    n = [0.0714, 0.0769, 0.0833, 0.0909, 0.1, 0.1111, 0.125, 0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

    ## Weighted B // 2/2, 2/3, 2/4...2/14
    # n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 7th number
    i = 13
    while i < len(allData):
      tempValues = allData[i-13:i+1]
      ema = 0.0
      dem = 0.0
      
      ## Go though list and calculate the EMA for the selected seven days
      for j, v in enumerate(tempValues):
        if v != -1:
          ema += (v * n[j])
          dem += n[j]
      
      if ema == 0:
        # expMA.append(None)
        expMA.append(expMA[-1])
      else:
        expMA.append(ema/dem)
      
      ## Go to next 7 days
      i += 1

    individualAvgData[param] = {
      "dates": allDates[13:],
      "averages": expMA
    }

  return individualAvgData, processedData


#### FUNCTION: calculates 7 DAY EXPONENTIAL // WEIGHTED moving average WITH Z-SCORE
def fourteenDayWeightedMovingAverageZScore(filecsv):
  processedData, individualData = zScoreAllData(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    ## make two lists, one for the data in past 90 days and other for all data collected
    allData = []
    ninetyData = []
    
    ## Initialize arrays for the moving average for each set of data
    maAll = []
    ma90 = []

    ## Fill allData -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        allData.append(data["zscoreAll"][idx])
        ninetyData.append(data["zscore90"][idx])
      else:
        ## Put -1 as filler to filter out later
        allData.append(-1)
        ninetyData.append(-1)

    ## Weighted B
    n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 13th number
    i = 13
    while i < len(allData):
      tempValuesAll = allData[i-13:i+1]
      emaAll = 0.0
      demAll = 0.0
      
      ## First go though list and calculate the moving average for the selected seven days for all data
      for j, v in enumerate(tempValuesAll):
        if v != -1:
          emaAll += (v * n[j])
          demAll += n[j]
      
      if emaAll == 0:
        # maAll.append(None)
        maAll.append(maAll[-1])
      else:
        maAll.append(emaAll/demAll)
      
      tempValues90 = ninetyData[i-13:i+1]
      ema90 = 0.0
      dem90 = 0.0

      ## Then go though list and calculate the moving average for the selected seven days for the 90 day data
      for j, v in enumerate(tempValues90):
        if v != -1:
          ema90 += (v * n[j])
          dem90 += n[j]
      
      if ema90 == 0:
        # ma90.append(None)
        ma90.append(ma90[-1])
      else:
        ma90.append(ema90/dem90)
      
      ## Go to next 7 days
      i += 1

    ## Averages using the z score
    individualAvgData[param] = {
      "dates": allDates[13:],
      "averagesAll": maAll,
      "averages90": ma90
    }
    ## 436 data points for each array above

  return individualAvgData, processedData


#### FUNCTION: calculates 7 DAY EXPONENTIAL // WEIGHTED moving average WITH Z-SCORE
def fourteenDayWeightedMovingAverageZScoreGP(filecsv):
  processedData, individualData = zScoreAllDataGP(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    if param != "total":
      ## make two lists, one for the data in past 90 days and other for all data collected
      allData = []
      
      ## Initialize arrays for the moving average for each set of data
      maAll = []

      ## Fill allData -1 for any value missing user data
      for date in allDates:
        if (date in data["dates"]):
          ## If date exists in the list, use the recorded data
          idx = data["dates"].index(date)
          allData.append(data["zscoreGP"][idx])
        else:
          ## Put -1 as filler to filter out later
          allData.append(-1)

      ## Weighted B
      n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

      ## Starting at the 13th number
      i = 13
      while i < len(allData):
        tempValuesAll = allData[i-13:i+1]
        emaAll = 0.0
        demAll = 0.0
        
        ## First go though list and calculate the moving average for the selected seven days for all data
        for j, v in enumerate(tempValuesAll):
          if v != -1:
            emaAll += (v * n[j])
            demAll += n[j]
        
        if emaAll == 0:
          # maAll.append(None)
          maAll.append(maAll[-1])
        else:
          maAll.append(emaAll/demAll)
        
        ## Go to next 14 days
        i += 1

    ## Averages using the z score
    individualAvgData[param] = {
      "dates": allDates[13:],
      "averagesGP": maAll,
    }
    ## 436 data points for each array above

  return individualAvgData, processedData


#### FUNCTION: calculates 7 DAY EXPONENTIAL // WEIGHTED moving average WITH Z-SCORE
def fourteenDayWeightedMovingAverageZScore90Days(filecsv):
  processedData, individualData = zScore90Days(filecsv)
  individualAvgData = {}
 
  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = processedData["total"]["dates"][0]
  endDate = processedData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in processedData.items():
    ninetyData = []
    ma90 = []

    ## Fill allData -1 for any value missing user data
    for date in allDates:
      if (date in data["dates"]):
        ## If date exists in the list, use the recorded data
        idx = data["dates"].index(date)
        ninetyData.append(data["zscore90"][idx])
      else:
        ## Put -1 as filler to filter out later
        ninetyData.append(-1)

    ## Weighted B
    n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 13th number
    i = 13
    while i < len(ninetyData):
      tempValues90 = ninetyData[i-13:i+1]
      ema90 = 0.0
      dem90 = 0.0

      ## Then go though list and calculate the moving average for the selected seven days for the 90 day data
      for j, v in enumerate(tempValues90):
        if v != -1:
          ema90 += (v * n[j])
          dem90 += n[j]
      
      if ema90 == 0:
        # ma90.append(None)
        ma90.append(ma90[-1])
      else:
        ma90.append(ema90/dem90)
      
      ## Go to next 7 days
      i += 1

    ## Averages using the z score
    individualAvgData[param] = {
      "dates": allDates[13:],
      "averages90": ma90
    }
    ## 436 data points for each array above

  return individualAvgData, processedData


# #### FUNCTION: takes moving average data and plots it with the form score
# def showMovingAverageAndTotalScore(filecsv, parameter):

#   #### This is for 7 POINT moving average
#   # avgData, processedData = sevenPointMovingAverage(filecsv)
#   # graphTitle = "Individual 7 Point Moving Average"
#   # filename = "_7PT_Moving_Average.png"
  
#   #### This is for 7 DAY moving average
#   # avgData, processedData = sevenDayMovingAverage(filecsv)
#   # graphTitle = "Individual 7 Day Moving Average"
#   # filename = "_7DAY_Moving_Average.png"

#   #### This is for 7 POINT EXPONENTIAL moving average
#   # avgData, processedData = sevenPointExponentialMovingAverage(filecsv)
#   # graphTitle = "Individual 7 Point Exponential Moving Average"
#   # filename = "_7PT_Exponential_Moving_Average.png"

#   #### This is for 7 POINT WEIGHTED moving average
#   # avgData, processedData = sevenPointWeightedMovingAverage(filecsv)
#   # graphTitle = "Individual 7 Point Weighted Moving Average"
#   # filename = "_7PT_Weighted_Moving_Average_OTHER.png"

#   #### This is for 7 DAY EXPONENTIAL moving average
#   # avgData, processedData = sevenDayExponentialMovingAverage(filecsv)
#   # graphTitle = "Individual 7 Day Exponential Moving Average"
#   # filename = "_7DAY_Exponential_Moving_Average.png"

#   #### This is for 7 DAY EXPONENTIAL moving average
#   # avgData, processedData = sevenDayExponentialMovingAverage(filecsv)
#   # graphTitle = "Individual 7 Day Weighted Moving Average"
#   # filename = "_B_7DAY_Weighted_Moving_Average.png"

#   #### This is for 7 DAY EXPONENTIAL moving average
#   # avgData, processedData = twentyEightDayExponentialMovingAverage(filecsv)
#   # graphTitle = "Individual 28 Day Moving Average"
#   # filename = "_B_28DAY_Moving_Moving_Average.png"

#   ## initialize the plot
#   fig, ax = plt.subplots()

#   if (parameter == 'fatigue'):
#     ## update data so its out of 100
#     values = [((v*100)/5) for v in avgData["fatigue"]["averages"]]
#     dates = avgData["fatigue"]["dates"]
#     ax.plot(dates, values, label='Fatigue')
#     # graphTitle += 'Fatigue '

#   elif (parameter == 'soreness'):
#     dates = avgData["soreness"]["dates"]
#     values = [((v*100)/5) for v in avgData["soreness"]["averages"]]
#     ax.plot(dates, values, label='Soreness')
#     # graphTitle += 'Soreness '

#   elif (parameter == 'stress'):
#     dates = avgData["stress"]["dates"]
#     values = [((v*100)/5) for v in avgData["stress"]["averages"]]
#     ax.plot(dates, values, label='Stress')
#     # graphTitle += 'Stress '

#   elif (parameter == 'sleepQuality'):
#     dates = avgData["sleepQuality"]["dates"]
#     values = [((v*100)/5) for v in avgData["sleepQuality"]["averages"]]
#     ax.plot(dates, values, label='SleepQuality')
#     # graphTitle += 'SleepQuality '

#   elif (parameter == 'hydration'):
#     dates = avgData["hydration"]["dates"]
#     values = [((v*100)/5) for v in avgData["hydration"]["averages"]]
#     ax.plot(dates, values, label='Hydration')
#     # graphTitle += 'Hydration '

#   elif (parameter == 'nutrition'):
#     dates = avgData["nutrition"]["dates"]
#     values = [((v*100)/5) for v in avgData["nutrition"]["averages"]]
#     ax.plot(dates, values, label='Nutrition')
#     # graphTitle += 'Nutrition '

#   elif (parameter == 'overall'):
#     dates = avgData["overall"]["dates"]
#     values = [((v*100)/5) for v in avgData["overall"]["averages"]]
#     ax.plot(dates, values, label='Overall')
#     # graphTitle += 'Overall '

#   ## Add the total form score 
#   totalDates = avgData["total"]["dates"]
#   totalValues = avgData["total"]["averages"]
#   ax.plot(totalDates, totalValues, label='Total Score')
#   # graphTitle += 'with Total Score '

#   ax.grid(True)
#   ax.set_ylim(0, 105)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=3)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Values')
#   ax.set_title(graphTitle)
  
#   plt.savefig(parameter + filename)
#   plt.show()


# #### FUNCTION: takes moving average data and plots it with the form score
# def showZscoreMovingAverageAndTotalScore(filecsv, parameter):

#   # #### This is for Z-SCORE of each category with form total 
#   # avgData, processedData = sevenDayWeightedMovingAverageWithZScore(filecsv)
#   # graphTitle = "Individual 7 Day Moving Average using All Data Z-Score"
#   # filename = "_A_all_7DAY_Moving_Moving_Average_ZScore.png"

#   # avgData, processedData = sevenDayWeightedMovingAverageWithZScore(filecsv)
#   # graphTitle = "Individual 7 Day Moving Average using All Data Z-Score"
#   # filename = "_B_all_7DAY_Moving_Moving_Average_ZScore.png"

#   #### This is for Z-SCORE of each category with form total 
#   # avgData, processedData = fourteenDayWeightedMovingAverage(filecsv)
#   # graphTitle = "Individual 14 Day Moving Average with All Data Z-Score"
#   # filename = "_A_all_14DAY_Moving_Moving_Average_ZScore.png"

#   # avgData, processedData = fourteenDayWeightedMovingAverage(filecsv)
#   # graphTitle = "Individual 14 Day Moving Average with All Data Z-Score"
#   # filename = "_B_all_14DAY_Moving_Moving_Average_ZScore.png"

#   ## initialize the plot
#   fig, ax = plt.subplots()

#   if (parameter == 'fatigue'):
#     ## update data so its out of 100
#     values = avgData["fatigue"]["averages"]
#     dates = avgData["fatigue"]["dates"]
#     ax.plot(dates, values, label='Fatigue')
#     # graphTitle += 'Fatigue '

#   elif (parameter == 'soreness'):
#     dates = avgData["soreness"]["dates"]
#     values = avgData["soreness"]["averages"]
#     ax.plot(dates, values, label='Soreness')
#     # graphTitle += 'Soreness '

#   elif (parameter == 'stress'):
#     dates = avgData["stress"]["dates"]
#     values = avgData["stress"]["averages"]
#     ax.plot(dates, values, label='Stress')
#     # graphTitle += 'Stress '

#   elif (parameter == 'sleepQuality'):
#     dates = avgData["sleepQuality"]["dates"]
#     values = avgData["sleepQuality"]["averages"]
#     ax.plot(dates, values, label='SleepQuality')
#     # graphTitle += 'SleepQuality '

#   elif (parameter == 'hydration'):
#     dates = avgData["hydration"]["dates"]
#     values = avgData["hydration"]["averages"]
#     ax.plot(dates, values, label='Hydration')
#     # graphTitle += 'Hydration '

#   elif (parameter == 'nutrition'):
#     dates = avgData["nutrition"]["dates"]
#     values = avgData["nutrition"]["averages"]
#     ax.plot(dates, values, label='Nutrition')
#     # graphTitle += 'Nutrition '

#   elif (parameter == 'overall'):
#     dates = avgData["overall"]["dates"]
#     values = avgData["overall"]["averages"]
#     ax.plot(dates, values, label='Overall')
#     # graphTitle += 'Overall '

#   ## Add the total form score 
#   totalDates = avgData["total"]["dates"]
#   totalValues = avgData["total"]["averages"]
#   ax.plot(totalDates, totalValues, label='Total Score')
#   # graphTitle += 'with Total Score '

#   ax.grid(True)
#   ax.set_ylim(-5.5, 5.5)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=3)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Values')
#   ax.set_title(graphTitle)
  
#   plt.savefig(parameter + filename)
#   plt.show()


# #### FUNCTION: takes moving average data and plots it with the form score
# def showZscore90DaysVsAllData(filecsv, parameter):

#   #### This is for Z-SCORE of each category 90 days vs all data
#   # avgData, processedData = sevenDayWeightedMovingAverageWithZScore(filecsv)
#   # graphTitle = "Individual 7 Day Moving Average, Z-Scores for "
#   # filename = "_90_All_7DAY_Moving_Average_ZScore.png"

#   #### This is for Z-SCORE of each category 90 days vs all data
#   avgData, processedData = fourteenDayWeightedMovingAverageZScore(filecsv)
#   graphTitle = "Individual 14 Day Moving Average, Z-Scores for "
#   filename = "_90_All_14DAY_Moving_Average_ZScore.png"

#   ## initialize the plot
#   fig, ax = plt.subplots()

#   if (parameter == 'fatigue'):
#     ## Add plot using all collected data
#     values = avgData["fatigue"]["averagesAll"]
#     dates = avgData["fatigue"]["dates"]
#     ax.plot(dates, values, label='Fatigue, All Data')

#     ## Add plot using 90 day data
#     values = avgData["fatigue"]["averages90"]
#     dates = avgData["fatigue"]["dates"]
#     ax.plot(dates, values, label='Fatigue, 90 Days')
    
#     graphTitle += 'Fatigue'

#   elif (parameter == 'soreness'):
#     ## Add plot using all collected data
#     values = avgData["soreness"]["averagesAll"]
#     dates = avgData["soreness"]["dates"]
#     ax.plot(dates, values, label='Soreness, All Data')

#     ## Add plot using 90 day data
#     values = avgData["soreness"]["averages90"]
#     dates = avgData["soreness"]["dates"]
#     ax.plot(dates, values, label='Soreness, 90 Days')
    
#     graphTitle += 'Soreness'

#   elif (parameter == 'stress'):
#     ## Add plot using all collected data
#     values = avgData["stress"]["averagesAll"]
#     dates = avgData["stress"]["dates"]
#     ax.plot(dates, values, label='Stress, All Data')

#     ## Add plot using 90 day data
#     values = avgData["stress"]["averages90"]
#     dates = avgData["stress"]["dates"]
#     ax.plot(dates, values, label='Stress, 90 Days')
    
#     graphTitle += 'Stress'

#   elif (parameter == 'sleepQuality'):
#     ## Add plot using all collected data
#     values = avgData["sleepQuality"]["averagesAll"]
#     dates = avgData["sleepQuality"]["dates"]
#     ax.plot(dates, values, label='SleepQuality, All Data')

#     ## Add plot using 90 day data
#     values = avgData["sleepQuality"]["averages90"]
#     dates = avgData["sleepQuality"]["dates"]
#     ax.plot(dates, values, label='SleepQuality, 90 Days')
    
#     graphTitle += 'SleepQuality'

#   elif (parameter == 'sleepQuantity'):
#     ## Add plot using all collected data
#     values = avgData["sleepQuantity"]["averagesAll"]
#     dates = avgData["sleepQuantity"]["dates"]
#     ax.plot(dates, values, label='sleepQuantity, All Data')

#     ## Add plot using 90 day data
#     values = avgData["sleepQuantity"]["averages90"]
#     dates = avgData["sleepQuantity"]["dates"]
#     ax.plot(dates, values, label='sleepQuantity, 90 Days')
    
#     graphTitle += 'sleepQuantity'


#   elif (parameter == 'hydration'):
#     ## Add plot using all collected data
#     values = avgData["hydration"]["averagesAll"]
#     dates = avgData["hydration"]["dates"]
#     ax.plot(dates, values, label='Hydration, All Data')

#     ## Add plot using 90 day data
#     values = avgData["hydration"]["averages90"]
#     dates = avgData["hydration"]["dates"]
#     ax.plot(dates, values, label='Hydration, 90 Days')
    
#     graphTitle += 'Hydration'

#   elif (parameter == 'nutrition'):
#     ## Add plot using all collected data
#     values = avgData["nutrition"]["averagesAll"]
#     dates = avgData["nutrition"]["dates"]
#     ax.plot(dates, values, label='Nutrition, All Data')

#     ## Add plot using 90 day data
#     values = avgData["nutrition"]["averages90"]
#     dates = avgData["nutrition"]["dates"]
#     ax.plot(dates, values, label='Nutrition, 90 Days')
    
#     graphTitle += 'Nutrition'

#   elif (parameter == 'overall'):
#     ## Add plot using all collected data
#     values = avgData["overall"]["averagesAll"]
#     dates = avgData["overall"]["dates"]
#     ax.plot(dates, values, label='Overall, All Data')

#     ## Add plot using 90 day data
#     values = avgData["overall"]["averages90"]
#     dates = avgData["overall"]["dates"]
#     ax.plot(dates, values, label='Overall, 90 Days')
    
#     graphTitle += 'Overall'

#   ax.grid(True)
#   ax.set_ylim(-5.5, 5.5)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=3)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Values')
#   ax.set_title(graphTitle)
  
#   plt.savefig(parameter + filename)
#   plt.show()


# #### FUNCTION: plot raw data with mean / max data to understand different 
# def showRawMeanMax(filecsv):
#   #### Load data from csv file 
#   dataRaw = loadData_oneUser(filecsv)

#   parameterName = 'overall'

#   datesRaw = dataRaw[parameterName]['dates']
#   valuesRaw = dataRaw[parameterName]['values']
#   datesUniqueSet = sorted(list(set(datesRaw)))

#   # Initializing lists to store unique dates and the corresponding values, using max or min filetering.
#   datesUnique = []
#   valuesUniqueMax = []
#   valuesUniqueMean = []

#   for i, date in enumerate(datesUniqueSet):

#     # Initialize tempValues
#     tempValues = []
#     # Find all values corresponding to the date
#     tempValues = [valuesRaw[j] for j, x in enumerate(datesRaw) if x == date]

#     # If data exists (which it)
#     if(len(tempValues)>0):

#       # Store unique date
#       datesUnique.append(date)
#       # Store mean of values
#       valuesUniqueMean.append(sum(tempValues)/float(len(tempValues)))
#       valuesUniqueMax.append(max(tempValues))


#   #### Plotting data
#   fig, ax = plt.subplots()
#   ax.plot(datesUnique, valuesUniqueMean, label='Unique Mean')
#   ax.plot(datesUnique, valuesUniqueMax, label='Unique Max')
#   ax.plot(datesRaw, valuesRaw, label='Raw Data')
#   ax.grid(True)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=4)
#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel(parameterName)
#   ax.set_title(parameterName)
#   plt.show()


# #### FUNCTION: takes params and plots on graph (timeseries)
# def individualParamTrend(filecsv, parameters):
#   individualData = dataPostMeanProcessing_oneUser(filecsv)

#   #### initialize all to false
#   params = {
#     'sleepQuality': 'false',
#     'hydration': 'false',
#     'nutrition': 'false',
#     'stress': 'false',
#     'fatigue': 'false',
#     'soreness': 'false',
#     'overall': 'false'
#   }

#   paramList = [p.strip() for p in parameters.split(',')]
#   for param in paramList:
#     graphParams[param] = 'true'

#   ## initialize the plot
#   fig, ax = plt.subplots()
#   graphTitle = "Individual (userId 4349) Trends for "

#   ## add all params indicated by user
#   ## each block adds a new plot to the figure
#   if (params['fatigue'] == 'true'):
#     dates = individualData["fatigue"]["dates"]
#     values = individualData["fatigue"]["values"]
#     ax.plot(dates, values, label='fatigue')
#     graphTitle += 'Fatigue '

#   if (params['soreness'] == 'true'):
#     dates = individualData["soreness"]["dates"]
#     values = individualData["soreness"]["values"]      
#     ax.plot(dates, values, label='soreness')
#     graphTitle += 'Soreness '

#   if (params['stress'] == 'true'):
#     dates = individualData["stress"]["dates"]
#     values = individualData["stress"]["values"] 
#     ax.plot(dates, values, label='stress')
#     graphTitle += 'Stress '

#   if (params['sleepQuality'] == 'true'):
#     dates = individualData["sleepQuality"]["dates"]
#     values = individualData["sleepQuality"]["values"] 
#     ax.plot(dates, values, label='sleepQuality')
#     graphTitle += 'SleepQuality '

#   if (params['hydration'] == 'true'):
#     dates = individualData["hydration"]["dates"]
#     values = individualData["hydration"]["values"] 
#     ax.plot(dates, values, label='hydration')
#     graphTitle += 'Hydration '

#   if (params['nutrition'] == 'true'):
#     dates = individualData["nutrition"]["dates"]
#     values = individualData["nutrition"]["values"] 
#     ax.plot(dates, values, label='nutrition')
#     graphTitle += 'Nutrition '

#   if (params['overall'] == 'true'):
#     dates = individualData["overall"]["dates"]
#     values = individualData["overall"]["values"] 
#     ax.plot(dates, values, label='overall')
#     graphTitle += 'Overall '

#   ax.grid(True)
#   ax.set_ylim(0, 5.5)   ## setting to 5.5 to give room at the top of the graph
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=3)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Values')
#   ax.set_title(graphTitle)
  
#   plt.show()


# #### FUNCTION: plots form score data on a graph (timeseries)
# def graphFormScore(filecsv, userId):

#   dataFormScore = dataWithFormScore(filecsv)
#   dates = dataFormScore["total"]["dates"]
#   values = dataFormScore["total"]["values"]

#   fig, ax = plt.subplots()
#   graphTitle = "Individual (userId " + userId +") Form Score"
#   dates = data["dates"]
#   values = data["values"]
#   ax.plot(dates, values, label='Form Score')

#   ax.grid(True)
#   ax.set_ylim(0, 100)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=3)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Form Score (total)')
#   ax.set_title(graphTitle)

#   plt.show()
  

# #### FUNCTION: plots parameter with formscore 
# def graphParamAndFormScore(filecsv, parameter):
#   individualData = dataWithFormScore(filecsv)

#   ## initialize the plot
#   fig, ax = plt.subplots()
#   graphTitle = "Individual Trends for "

#   if (parameter == 'fatigue'):
#     ## update data so its out of 100
#     values = [((v*100)/5) for v in individualData["fatigue"]["values"]]
#     dates = individualData["fatigue"]["dates"]
#     ax.plot(dates, values, label='fatigue')
#     graphTitle += 'Fatigue '

#   elif (parameter == 'soreness'):
#     dates = individualData["soreness"]["dates"]
#     values = [((v*100)/5) for v in individualData["soreness"]["values"]]
#     ax.plot(dates, values, label='soreness')
#     graphTitle += 'Soreness '

#   elif (parameter == 'stress'):
#     dates = individualData["stress"]["dates"]
#     values = [((v*100)/5) for v in individualData["stress"]["values"]]
#     ax.plot(dates, values, label='stress')
#     graphTitle += 'Stress '

#   elif (parameter == 'sleepQuality'):
#     dates = individualData["sleepQuality"]["dates"]
#     values = [((v*100)/5) for v in individualData["sleepQuality"]["values"]]
#     ax.plot(dates, values, label='sleepQuality')
#     graphTitle += 'SleepQuality '

#   elif (parameter == 'hydration'):
#     dates = individualData["hydration"]["dates"]
#     values = [((v*100)/5) for v in individualData["hydration"]["values"]]
#     ax.plot(dates, values, label='hydration')
#     graphTitle += 'Hydration '

#   elif (parameter == 'nutrition'):
#     dates = individualData["nutrition"]["dates"]
#     values = [((v*100)/5) for v in individualData["nutrition"]["values"]]
#     ax.plot(dates, values, label='nutrition')
#     graphTitle += 'Nutrition '

#   elif (parameter == 'overall'):
#     dates = individualData["overall"]["dates"]
#     values = [((v*100)/5) for v in individualData["overall"]["values"]]
#     ax.plot(dates, values, label='overall')
#     graphTitle += 'Overall '

#   ## Add the total form score 
#   totalDates = individualData["total"]["dates"]
#   totalValues = individualData["total"]["values"]
#   ax.plot(totalDates, totalValues, label='Total Score')
#   graphTitle += 'with Total Score '

#   ax.grid(True)
#   ax.set_ylim(0, 105)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=3)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Values')
#   ax.set_title(graphTitle)
  
#   plt.savefig(parameter + "_with_form_score.png")
#   plt.show()


# #### FUNCTION: correlation coeffiecent for params vs overall
# def correlationCoeffiecent(filecsv, parameter):
  
#   avgData, processedData = sevenDayWeightedMovingAverageWithZScore(filecsv)

#   r = np.corrcoef(avgData[parameter]["averagesAll"], avgData["overall"]["averagesAll"])[0,1]

#   print "Correlation coeffiecent for " + parameter + " is "
#   print r
#   return r


# def graphScatterPlot(filecsv, parameter1, parameter2):
#   # avgData, processedData = sevenDayWeightedMovingAverageWithZScore(filecsv)
#   avgData, processedData = fourteenDayWeightedMovingAverageZScore(filecsv)

#   x = avgData[parameter1]["averagesAll"]
#   y = avgData[parameter2]["averagesAll"]
#   graphTitle = "14 Day Weighted Moving Average Z-Score, " + parameter1 + " and " + parameter2

#   r = np.corrcoef(avgData[parameter1]["averagesAll"], avgData[parameter2]["averagesAll"])[0,1]

#   N = 4
#   colors = np.random.rand(N)
#   area = 120

#   fig, ax = plt.subplots()

#   ax.grid(True)

#   ax.text(0.95, 0.01, 'r = ' + str(r),
#         verticalalignment='bottom', horizontalalignment='right',
#         transform=ax.transAxes,
#         color='black', fontsize=20)
  
#   ## set axes and title
#   ax.set_title(graphTitle)

#   ax.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
#   ax.scatter(x, y, s=area, c=colors, alpha=0.5)

#   plt.savefig("14DAY_" + parameter1 + "_" + parameter2+ "_scatter_plot.png")
#   # plt.show()


# #### FUNCTION: scatterplot for correlation
# def createScatterPlotDF(filecsv):
#   processedData = dataWithFormScore(filecsv)

#   ## Multiply all of the regular params by 20 so it can be compared to the total score
#   # d = {
#   #   "fatigue": [i * 20 for i in processedData["fatigue"]["values"]],
#   #   "soreness": [i * 20 for i in processedData["soreness"]["values"]],
#   #   "stress": [i * 20 for i in processedData["stress"]["values"]],
#   #   "sleepQuality": [i * 20 for i in processedData["sleepQuality"]["values"]],
#   #   "nutrition": [i * 20 for i in processedData["nutrition"]["values"]],
#   #   "hydration": [i * 20 for i in processedData["hydration"]["values"]],
#   #   "overall": [i * 20 for i in processedData["overall"]["values"]],
#   #   "total": processedData["total"]["values"]
#   # }

#   d = {
#     "fatigue": processedData["fatigue"]["values"],
#     "soreness": processedData["soreness"]["values"],
#     # "stress": processedData["stress"]["values"],
#     # "sleepQuality": processedData["sleepQuality"]["values"],
#     # "nutrition": processedData["nutrition"]["values"],
#     # "hydration": processedData["hydration"]["values"],
#     # "overall": processedData["overall"]["values"],
#     # "total": [i / 20 for i in processedData["total"]["values"]]
#   }

#   df = pd.DataFrame(data=d)

#   # print df

#   fig = ff.create_scatterplotmatrix(df, height=1000, width=1000)
#   py.iplot(fig, filename='parameters_matrix_scatterplot_2')


##########################################################################################
##########################################################################################
##########################################################################################


#### FUNCITON: calculates the zscore for each parameter 
#### using the personal history (PH)
def zScorePH90Days(filecsv):
  processedData = dataWithFormScore(filecsv)
  # print processedData["fatigue"]["dates"]
  
  ## Initialize object to return with all data points
  individualAvgData = {}
 
  for param, data in processedData.items():

    ## Initialize the lists to hold personal history data
    meanPH = []
    stdPH = []

    for d in data["dates"]:
      
      ## For each date, get the mean and std for the past 90 days
      ninetyDaysAgo = (d - datetime.timedelta(days = 90))
      ninetyDayData = []
      
      ## Go through dates again to find the values in past 90 days
      for j, innerDate in enumerate(data["dates"]):
        if ((innerDate < d) and (innerDate > ninetyDaysAgo)):

          ## Add the value to the 90 day list
          ninetyDayData.append(data["values"][j])

      ## Get the mean and standard deviation using data from past 90 days
      meanPH.append(np.mean(ninetyDayData))
      stdPH.append(np.std(ninetyDayData))


    individualAvgData[param] = {
      "dates": data["dates"],
      "values": data["values"],
      "meanPH": meanPH,
      "stdPH": stdPH
    }

  # Add z-score for the 90 day avg and std
  for param, data in individualAvgData.items():
    
    ## Initialize the z-score list 
    zscoreData = []

    for i, d in enumerate(data["dates"]):
      if data["stdPH"][i] == 0:
        zscoreData.append(0)
      else: 
        zscore = (data["values"][i] - data["meanPH"][i]) / data["stdPH"][i]
        zscoreData.append(zscore)

    ## Add z-score to the data in the object to return
    individualAvgData[param]["zscorePH"] = zscoreData

  ## Returns object of parameters with dates, score values, means, stds, and z-scores using the 90 day personal history
  return individualAvgData


#### FUNCITON: calculates the zscore for each parameter 
#### using the general population data (GP)
def zScoreAllDataGP(filecsv):

  ## Already have the PH data from this function
  individualAvgData = zScorePH90Days(filecsv)

  with open('paramId_std_avg.csv') as generalPopData:
    csvReader = csv.reader(generalPopData)

    for row in csvReader:
      ## Add the std and mean for general population, note this is an int NOT a list
      individualAvgData[str(row[0])]["stdGP"] = float(row[1])
      individualAvgData[str(row[0])]["meanGP"] = float(row[2])

  # Add z-score for all data avg and std
  for param, data in individualAvgData.items():
    
    ## Don't want to include total because don't have total for the general population
    if param != "total":
      zscoreDataTemp = []
    
      for i, d in enumerate(data["dates"]):

        ## Calculate the score for each date using the general population data
        zscore = (data["values"][i] - data["meanGP"]) / data["stdGP"]
        zscoreDataTemp.append(zscore)

      ## Add the z-score for general population data
      individualAvgData[param]["zscoreGP"] = zscoreDataTemp

  return individualAvgData


#### FUNCTION: calculates the 14 day weighted moving average of the z-score using the PH data
def fourteenDayWeightedMovingAverageZScorePH(filecsv):
  ## Get the z-score data for PH and GP, just configuring the PH moving avg here
  individualAvgData = zScoreAllDataGP(filecsv)

  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = individualAvgData["total"]["dates"][0]
  endDate = individualAvgData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in individualAvgData.items():
    ## Initialize the list to hold the z-score
    tempZscores = []
    
    ## Initialize array
    tempMovingAverages = []

    ## Fill with -1 for any value missing recorded user data
    for date in allDates:
      ## If date exists in the parameter's date list, use the recorded data
      if (date in data["dates"]):
        idx = data["dates"].index(date)
        tempZscores.append(data["zscorePH"][idx])
      else:
        ## Put -1 as filler to filter out later
        tempZscores.append(-1)

    ## Weighted B
    n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Starting at the 13th number
    i = 13
    while i < len(tempZscores):
      tempValuesAll = tempZscores[i-13:i+1]
      weightedSum = 0.0
      totalCoefficient = 0.0
      
      ## First go though list and calculate the moving average for the selected seven days for all data
      for j, v in enumerate(tempValuesAll):
        if v != -1:
          weightedSum += (v * n[j])
          totalCoefficient += n[j]
      
      if weightedSum == 0:
        tempMovingAverages.append(tempMovingAverages[-1])
      else:
        tempMovingAverages.append(weightedSum/totalCoefficient)
      
      ## Go to next 14 days
      i += 1

    ## Add averages using the z score from personal history data
    individualAvgData[param]["datesMovingAveragePH"] = allDates[13:]
    individualAvgData[param]["weightedMovingAveragePH"] = tempMovingAverages

  return individualAvgData


#### FUNCTION: calculates the 14 day weighted moving average of the z-score using the GP data
def fourteenDayWeightedMovingAverageZScoreGP(filecsv):
  ## Get the z-score data for PH and GP, just configuring the PH moving avg here
  individualAvgData = fourteenDayWeightedMovingAverageZScorePH(filecsv)

  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = individualAvgData["total"]["dates"][0]
  endDate = individualAvgData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in individualAvgData.items():
    if param != "total":
      ## Initialize the list to hold the z-score
      tempZscores = []
      
      ## Initialize array
      tempMovingAverages = []

      ## Fill with -1 for any value missing recorded user data
      for date in allDates:
        ## If date exists in the parameter's date list, use the recorded data
        if (date in data["dates"]):
          idx = data["dates"].index(date)
          tempZscores.append(data["zscoreGP"][idx])
        else:
          ## Put -1 as filler to filter out later
          tempZscores.append(-1)

      ## Weighted B
      n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

      ## Starting at the 13th number
      i = 13
      while i < len(tempZscores):
        tempValuesAll = tempZscores[i-13:i+1]
        weightedSum = 0.0
        totalCoefficient = 0.0
        
        ## First go though list and calculate the moving average for the selected seven days for all data
        for j, v in enumerate(tempValuesAll):
          if v != -1:
            weightedSum += (v * n[j])
            totalCoefficient += n[j]
        
        if weightedSum == 0:
          tempMovingAverages.append(tempMovingAverages[-1])
        else:
          tempMovingAverages.append(weightedSum/totalCoefficient)
        
        ## Go to next 14 days
        i += 1

      ## Add averages using the z score from personal history data
      individualAvgData[param]["datesMovingAverageGP"] = allDates[13:]
      individualAvgData[param]["weightedMovingAverageGP"] = tempMovingAverages

  return individualAvgData


#### FUNCTION: calculate bridge score for each parameter and total score (personal history only)
def calculatePersonalHistoryBridgeScore(filecsv):
  ## Returns object with: dates, scores, meanPH, stdPh, meanGP, stdGP, zscorePH, datesMovingAveragePH, weightedMovingAveragePH, 
  ## zscoreGP, datesMovingAverageGP, weightedMovingAverageGP
  individualData = fourteenDayWeightedMovingAverageZScoreGP(filecsv)

  for param, data in individualData.items():
    ## Approximating e = 2.718281
    bridgeScorePersonalHistory = [(3/(3+((np.power([2.718281], [-x]))[0]))) for x in data["weightedMovingAveragePH"]]

    individualData[param]["bridgeScorePH"] = bridgeScorePersonalHistory

  return individualData


#### FUNCTION: calculate bridge score for each parameter and total score
def calculateGeneralPopulationBridgeScore(filecsv):
  ## Returns object with: dates, scores, meanPH, stdPh, meanGP, stdGP, zscorePH, datesMovingAveragePH, weightedMovingAveragePH, 
  ## zscoreGP, datesMovingAverageGP, weightedMovingAverageGP and bridgeScorePH
  individualData = calculatePersonalHistoryBridgeScore(filecsv)

  for param, data in individualData.items():
    if param != "total":
      bridgeScorePersonalHistory = [(3/(3+((np.power([2.718281], [-x]))[0]))) for x in data["weightedMovingAverageGP"]]

      individualData[param]["bridgeScoreGP"] = bridgeScorePersonalHistory

  return individualData


#### FUNCTION: user personal history score and general populations score for bridge score for one user
def calculateBridgeScore(filecsv):
  individualData = calculateGeneralPopulationBridgeScore(filecsv)

  for param, data in individualData.items():
    dataBridgeScore = []
    
    ## Need to find a way to get total for the GP 
    if param != "total":

      ## Can assume that the date exists in general population because this user is in the general population
      for i, d in enumerate(data["datesMovingAveragePH"]):
        dataBridgeScore.append(((0.67*(data["bridgeScorePH"][i])) + (0.33*(data["bridgeScoreGP"][i]))) * 100)
      
      individualData[param]["bridgeScore"] = dataBridgeScore
  return individualData


#### FUNCTION: create table of scores for each parameter
def tableBridgeScores(filecsv):
  bridgeScoreData = calculateBridgeScore(filecsv)

  with open('bridgeScores_user_4349.csv', 'wb') as bridgeScoreTable:
    writer = csv.writer(bridgeScoreTable)
    dates = copy.deepcopy(bridgeScoreData["fatigue"]["datesMovingAveragePH"][89:])
    
    ## want first cell to be empty so just add today's date
    dates.insert(0, datetime.datetime.now())
    writer.writerow([datetime.date.isoformat(d) for d in dates])

    for param, data in bridgeScoreData.items():
      if param != "total":
        scoreData = copy.deepcopy(data["bridgeScore"][89:])
        scoreData.insert(0, param)
        writer.writerow([(round((x*1.0),4)) if (isinstance(x, float) or isinstance(x, int)) else x for x in scoreData])


#### FUNCTION: show bridge score for all parameters and total score over time (personal history only)
def graphBridgeScore(filecsv):
  bridgeScoreData = calculateBridgeScore(filecsv)

  fig, ax = plt.subplots()
  graphTitle = "Bridge Score"

  for param, data in bridgeScoreData.items():
    if param != "total":
      values = bridgeScoreData[param]["bridgeScore"][89:]
      dates = bridgeScoreData[param]["datesMovingAveragePH"][89:]
      ax.plot(dates, values, label=param)

  ax.grid(True)
  ax.set_ylim(0, 105)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=4)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Bridge Score (%)')
  ax.set_title(graphTitle)

  plt.show()



##########################################################################################
##########################################################################################
##########################################################################################







# #### FUNCTION: create table of scores for each parameter
# def tablePersonalHistoryBridgeScores(filecsv):
#   bridgeScoreData = calculateBridgeScore(filecsv)

#   with open('bridgeScores_user_4349.csv', 'wb') as bridgeScoreTable:
#     writer = csv.writer(bridgeScoreTable)
#     dates = copy.deepcopy(bridgeScoreData["fatigue"]["datesMovingAveragePH"])
#     ## want first cell to be empty so just add today's date
#     dates.insert(0, datetime.datetime.now())
#     writer.writerow([datetime.date.isoformat(d) for d in dates])

#     for param, data in bridgeScoreData.items():
#       data["bridgeScore"].insert(0, param)
#       writer.writerow([(round((x*1.0),4)) if (isinstance(x, float) or isinstance(x, int)) else x for x in data["bridgeScorePH"]])


# #### FUNCTION: show bridge score for all parameters and total score over time (personal history only)
# def graphBridgeScorePH(filecsv):
#   bridgeScoreData = calculatePersonalHistoryBridgeScore(filecsv)
 
#   # dates = dataFormScore["total"]["dates"]
#   # values = dataFormScore["total"]["bridgeScorePH"]

#   fig, ax = plt.subplots()
#   graphTitle = "Bridge Score (Personal History Data)"

#   # for param, data in bridgeScoreData.items():
#   values = bridgeScoreData["overall"]["bridgeScorePH"]
#   dates = bridgeScoreData["overall"]["dates"]
#   ax.plot(dates, values, label="Overall")

#   values = bridgeScoreData["total"]["bridgeScorePH"]
#   dates = bridgeScoreData["total"]["dates"]
#   ax.plot(dates, values, label="Total")


#   ax.grid(True)
#   ax.set_ylim(0, 105)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=4)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Bridge Score (%)')
#   ax.set_title(graphTitle)

#   plt.savefig("Overall_Bridge_Score.png")
#   plt.show()





















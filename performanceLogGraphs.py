# SELECT userId, parameterId, UNIX_TIMESTAMP(recordedAt), intValue 
# FROM userparameter 
# WHERE userId in (4349) 
# AND formquestionid in (103, 104, 105, 106, 107, 108, 109) 
# LIMIT 100000;

# SELECT DATE(aup.createdAt) AS createdAt, aup.parameterId, AVG(aup.avgIntValue) AS gpIntValue
#   FROM (SELECT DATE(createdAt) AS createdAt, userId, parameterId, AVG(intValue) AS avgIntValue 
#       FROM userparameter 
#       WHERE userId > 0 AND intValue > 0 AND parameterId IN (492,493,494,495,496,497,498,614)
#       GROUP BY userId, DATE(createdAt), parameterId) AS aup
#   WHERE userId > 0 
#   GROUP BY DATE(createdAt), parameterId;


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
#### NOTE: this function organizes raw data and does not convert to scores
#### NOTE: not in use for calculating the bridge score
# def loadData_oneUser(filecsv):

#   ## empty dictionary to be filled with performance log data
#   individualPerformanceLogData = {
#     "fatigue": {
#       "dates": [],
#       "values": []
#     },
#     "soreness": {
#       "dates": [],
#       "values": []
#     },
#     "stress": {
#       "dates": [],
#       "values": []
#     },
#     "sleepQuality": {
#       "dates": [],
#       "values": []
#     },
#     "sleepQuantity": {
#       "dates": [],
#       "values": []
#     },
#     "nutrition": {
#       "dates": [],
#       "values": []
#     },
#     "hydration": {
#       "dates": [],
#       "values": []
#     },
#     "overall": {
#       "dates": [],
#       "values": []
#     }
#   }

#   with open(filecsv) as performanceLogData:
#     csvReader = csv.reader(performanceLogData)

#     for row in csvReader:
#       ## convert date to YYYY-MM-DD
#       date = datetime.date.fromtimestamp(int(row[2]))
      
#       ## fatigue data; parameterId 492
#       if (int(row[1]) == 492):
#         individualPerformanceLogData["fatigue"]["dates"].append(date)
#         individualPerformanceLogData["fatigue"]["values"].append(int(row[3]))
      
#       ## soreness data; parameterId 493
#       if (int(row[1]) == 493):
#         individualPerformanceLogData["soreness"]["dates"].append(date)
#         individualPerformanceLogData["soreness"]["values"].append(int(row[3]))
      
#       ## stress data; parameterId 494
#       if (int(row[1]) == 494):
#         individualPerformanceLogData["stress"]["dates"].append(date)
#         individualPerformanceLogData["stress"]["values"].append(int(row[3]))
      
#       ## sleepQuality data; parameterId 495
#       if (int(row[1]) == 495):
#         individualPerformanceLogData["sleepQuality"]["dates"].append(date)
#         individualPerformanceLogData["sleepQuality"]["values"].append(int(row[3]))

#       ## sleepQuantity data; parameterId 614
#       if (int(row[1]) == 495):
#         individualPerformanceLogData["sleepQuantity"]["dates"].append(date)
#         individualPerformanceLogData["sleepQuantity"]["values"].append((int(row[3]))/1000.0)
      
#       ## nutrition data; parameterId 496
#       if (int(row[1]) == 496):
#         individualPerformanceLogData["nutrition"]["dates"].append(date)
#         individualPerformanceLogData["nutrition"]["values"].append(int(row[3]))
      
#       ## hydration data; parameterId 497
#       if (int(row[1]) == 497):
#         individualPerformanceLogData["hydration"]["dates"].append(date)
#         individualPerformanceLogData["hydration"]["values"].append(int(row[3]))
      
#       ## overall data; parameterId 498
#       if (int(row[1]) == 498):
#         individualPerformanceLogData["overall"]["dates"].append(date)
#         individualPerformanceLogData["overall"]["values"].append(int(row[3]))

#   return individualPerformanceLogData


#### FUNCTION: takes a csv file with performance log data for one user 
#### NOTE: this function organizes question scores 
#### NOTE: used to load in data for the Bridge Score
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
        ## calculate score for fatigue out of 100
        score = ((6 - int(row[3])) * 20)
        individualPerformanceLogScores["fatigue"]["values"].append(score)
      
      ## soreness data; parameterId 493
      if (int(row[1]) == 493):
        individualPerformanceLogScores["soreness"]["dates"].append(date)
        ## calculate score for soreness
        score = ((6 - int(row[3])) * 20)
        individualPerformanceLogScores["soreness"]["values"].append(score)
      
      ## stress data; parameterId 494
      if (int(row[1]) == 494):
        individualPerformanceLogScores["stress"]["dates"].append(date)
        ## calculate score for sleepQuality
        score = ((6 - int(row[3])) * 20)
        individualPerformanceLogScores["stress"]["values"].append(score)
      
      ## sleepQuality data; parameterId 495
      if (int(row[1]) == 495):
        individualPerformanceLogScores["sleepQuality"]["dates"].append(date)
        individualPerformanceLogScores["sleepQuality"]["values"].append((int(row[3])) * 20)
      
      ## sleepQuantity data; parameterId 614
      if (int(row[1]) == 614):
        score = 0
        intValue = ((int(row[3]))/1000.0)
        if (intValue >= 9):
          score = 100
        elif (intValue >= 8 and intValue < 9):
          score = 90
        elif (intValue >= 7 and intValue < 8):
          score = 80
        elif (intValue >= 6 and intValue < 7):
          score = 70
        elif (intValue >= 5 and intValue < 6):
          score = 55
        elif (intValue >= 4 and intValue < 5):
          score = 40
        else:
          score = 0
        
        individualPerformanceLogScores["sleepQuantity"]["dates"].append(date)
        individualPerformanceLogScores["sleepQuantity"]["values"].append(score)

      ## nutrition data; parameterId 496
      if (int(row[1]) == 496):
        individualPerformanceLogScores["nutrition"]["dates"].append(date)
        individualPerformanceLogScores["nutrition"]["values"].append((int(row[3])) * 20)
      
      ## hydration data; parameterId 497
      if (int(row[1]) == 497):
        individualPerformanceLogScores["hydration"]["dates"].append(date)
        individualPerformanceLogScores["hydration"]["values"].append((int(row[3])) * 20)
      
      ## overall data; parameterId 498
      if (int(row[1]) == 498):
        individualPerformanceLogScores["overall"]["dates"].append(date)
        individualPerformanceLogScores["overall"]["values"].append((int(row[3])) * 20)

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


#### FUNCTION: calculates form score out of 100 pt scale
#### Includes hours of sleep
def dataWithFormScore(filecsv):
  
  processedData = dataPostMeanProcessing_oneUser(filecsv)
  
  ## Initialize the total arrays
  processedData["total"] = {
    "dates": [],
    "values": []
  }

  ## Initalize comprehensive list to hold dates
  allDates = []
  
  ## build comprehensive array with all dates from each param list
  for param, data in processedData.items():
    allDates += data['dates']

  uniqueAllDates = sorted(list(set(allDates)))
  
  for uniqueDate in uniqueAllDates:
    
    ## Initialize to hold the values for each date
    sumValue = 0
    numParams = 0
    
    for param, data in processedData.items():
      if uniqueDate in data["dates"]:
        idx = data["dates"].index(uniqueDate)
        
        ## Map hours of sleep to score off 100
        ## Update this to use ln(x) function 
        if param == "sleepQuantity":
          if (data["values"][idx] >= 9):
            sumValue += 100
            numParams += 1
          elif (data["values"][idx] >= 8 and data["values"][idx] < 9):
            sumValue += 90
            numParams += 1
          elif (data["values"][idx] >= 7 and data["values"][idx] < 8):
            sumValue += 80
            numParams += 1
          elif (data["values"][idx] >= 6 and data["values"][idx] < 7):
            sumValue += 70
            numParams += 1
          elif (data["values"][idx] >= 5 and data["values"][idx] < 6):
            sumValue += 55
            numParams += 1
          elif (data["values"][idx] >= 4 and data["values"][idx] < 5):
            sumValue += 40
            numParams += 1
          else:
            sumValue += 0
            numParams += 1

        elif param != "sleepQuantity":
          sumValue += (data["values"][idx])
          numParams += 1

    processedData["total"]["dates"].append(uniqueDate)
    maxPts = numParams*100
    processedData["total"]["values"].append((sumValue*100)/maxPts)

  return processedData


# #### FUNCTION: calculates and shows number of questions answered for each form submission
# def questionsAnsweredPerSubmission(filecsv):
#   # go through all dates from total score
#   # add one if the date exists in each parameter

#   processedData = dataWithFormScore(filecsv)

#   ## Already went through and got all dates that have one or more response recorded
#   dates = processedData["total"]["dates"]
#   numResponses = []

#   for date in dates:
#     answers = 0
#     for param, data in processedData.items(): 
#       if param != "total":
#         if date in data["dates"]:
#           answers += 1

#     numResponses.append(answers)

#   fig, ax = plt.subplots()
#   graphTitle = "Number of Questions Answered per Form Submission (max. 8)"
#   ax.plot(dates, numResponses, label='Num. Questions Answered')

#   ax.grid(True)
#   ax.set_ylim(0, 8.5)
#   ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
#   fig.autofmt_xdate()
#   ax.legend(loc=3)

#   ## set axes and title
#   ax.set_xlabel('Dates')
#   ax.set_ylabel('Num. Questions Answered')
#   ax.set_title(graphTitle)

#   plt.savefig("Responses_per_submission.png")
#   plt.show()


# #### FUNCTION: calculates 7 PT moving average
# def sevenPointMovingAverage(filecsv):
#   processedData = dataWithFormScore(filecsv)
  
#   individualAvgData = {}

#   for param, data in processedData.items():

#     ## Initializing list to convolve with question scores
#     n = [1,1,1,1,1,1,1]

#     ## Get moving sum
#     preAverages = np.convolve(data["values"], n, mode='valid')

#     ## Divide all items by 7 to get moving average
#     averages = [x/7 for x in preAverages]

#     ## Additional calculations needed if switch convolve mode to full
#     # averages = [x/(n+1) if n+1 < 7 else x/7 for n, x in enumerate(preAverages)]

#     individualAvgData[param] = {
#       ## Remove the first 6 dates since we are using convolve mode = valid
#       "dates": data["dates"][6:],
#       "averages": averages
#     }

#   return individualAvgData, processedData


# #### FUNCTION: calculates 7 PT EXPONENTIAL moving average
# def sevenPointExponentialMovingAverage(filecsv):
#   processedData = dataWithFormScore(filecsv)
  
#   individualAvgData = {}

#   for param, data in processedData.items():

#     ## Initializing list to convolve with question scores
#     ## the np.convolve function will invert this list
#     n = [1,0.5,0.25,0.125,0.0625,0.03125,0.015625]

#     ## Get moving sum
#     preAverages = np.convolve(data["values"], n, mode='valid')

#     ## Divide all items by 7 to get moving average
#     averages = [x/(sum(n)) for x in preAverages]

#     individualAvgData[param] = {
#       ## Remove the first 6 dates since we are using convolve mode = valid
#       "dates": data["dates"][6:],
#       "averages": averages
#     }

#   return individualAvgData, processedData


# #### FUNCTION: calculates 7 PT WEIGHTED moving average in slightly different way
# def sevenPointWeightedMovingAverage(filecsv):
#   ## Get the simple 7 point moving average
#   avgData, processedData = sevenPointMovingAverage(filecsv)

#   individualAvgData = {}
 
#   ## Want a 7 point moving average
#   n = 7
  
#   ## Get multiplier, force the float
#   k = 2.0/(n+1)

#   for param, data in processedData.items():
#     firstMA = avgData[param]["averages"][0]
#     expMA = []

#     for i, d in enumerate(data["values"]):
#       ## Initialize exponential moving average (ema)
#       ema = 0

#       ## Use the simple moving average for first data point
#       if i == 0:
#         ema = ((d - firstMA) * k) + firstMA

#       ## Otherwise use EMA = ((Current price - Previous EMA) * k) + Previous EMA
#       else:
#         ema = ((d - expMA[-1]) * k) + expMA[-1]
     
#       expMA.append(ema)

#     individualAvgData[param] = {
#       "dates": data["dates"],
#       "averages": expMA
#     }

#   return individualAvgData, processedData


# #### FUNCTION: calculates 7 DAY moving average
# def sevenDayMovingAverage(filecsv):
#   processedData = dataWithFormScore(filecsv)

#   individualAvgData = {}

#   ## list is already sorted, so take the first and last date of ["total"]["dates"]
#   startDate = processedData["total"]["dates"][0]
#   endDate = processedData["total"]["dates"][-1]

#   ## Get every date between start and end date
#   allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

#   for param, data in processedData.items():
#     allData = []

#     ## Get a list of data with -1 for any value missing user data
#     for date in allDates:
#       if (date in data["dates"]):
#         ## If date exists in the list, use the recorded data
#         idx = data["dates"].index(date)
#         allData.append(data["values"][idx])
#       else:
#         ## Put -1 as filler to filter out later
#         allData.append(-1)

#     n = [1,1,1,1,1,1,1]
#     preAverages = np.convolve(allData, n, mode='valid')

#     movingAverage = []
#     ## Go through and find out what the denominator should be
#     for i, x in enumerate(preAverages):

#       ## Get the seven values that contributed to this data point
#       tempValues = allData[i:(i+7)]

#       ## Find out how many should be filtered out
#       filtered = tempValues.count(-1)
#       dataPoints = (7 - filtered)

#       if dataPoints == 0:
#         ## If there were no data points in the seven days, take the average from the previous day
#         movingAverage.append(movingAverage[-1])
#       else:
        
#         ## Add sum / actual number of data points that contributed
#         movingAverage.append((x+filtered)/dataPoints)

#     individualAvgData[param] = {
#       "dates": allDates[6:],
#       "averages": movingAverage
#     }

#   return individualAvgData, processedData


# #### FUNCTION: calculates 7 DAY EXPONENTIAL // WEIGHTED moving average
# def sevenDayExponentialMovingAverage(filecsv):
#   processedData = dataWithFormScore(filecsv)
#   individualAvgData = {}
 
#   ## list is already sorted, so take the first and last date of ["total"]["dates"]
#   startDate = processedData["total"]["dates"][0]
#   endDate = processedData["total"]["dates"][-1]

#   ## Get every date between start and end date
#   allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

#   for param, data in processedData.items():
#     allData = []
#     expMA = []

#     ## Fill allData -1 for any value missing user data
#     for date in allDates:
#       if (date in data["dates"]):
#         ## If date exists in the list, use the recorded data
#         idx = data["dates"].index(date)
#         allData.append(data["values"][idx])
#       else:
#         ## Put -1 as filler to filter out later
#         allData.append(-1)


#     ### Exponential
#     # n = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

#     ## Weighted A
#     n = [0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

#     ## Weighted B
#     # n = [0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

#     ## Starting at the 7th number
#     i = 6
#     while i < len(allData):
#       tempValues = allData[i-6:i+1]
#       ema = 0.0
#       dem = 0.0
      
#       ## Go though list and calculate the EMA for the selected seven days
#       for j, v in enumerate(tempValues):
#         if v != -1:
#           ema += (v * n[j])
#           dem += n[j]
      
#       if ema == 0:
#         # expMA.append(None)
#         expMA.append(expMA[-1])
#       else:
#         expMA.append(ema/dem)
      
#       ## Go to next 7 days
#       i += 1

#     individualAvgData[param] = {
#       "dates": allDates[6:],
#       "averages": expMA
#     }

#   return individualAvgData, processedData


# #### FUNCTION: calculates 28 DAY WEIGHTED moving average
# def twentyEightDayExponentialMovingAverage(filecsv):
#   processedData = dataWithFormScore(filecsv)
#   individualAvgData = {}
 
#   ## list is already sorted, so take the first and last date of ["total"]["dates"]
#   startDate = processedData["total"]["dates"][0]
#   endDate = processedData["total"]["dates"][-1]

#   ## Get every date between start and end date
#   allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

#   for param, data in processedData.items():
#     allData = []
#     expMA = []

#     ## Fill allData -1 for any value missing user data
#     for date in allDates:
#       if (date in data["dates"]):
#         ## If date exists in the list, use the recorded data
#         idx = data["dates"].index(date)
#         allData.append(data["values"][idx])
#       else:
#         ## Put -1 as filler to filter out later
#         allData.append(-1)


#     ### Exponential
#     # n = [ 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

#     ## Weighted A // 1/2, 1/3...1/14
#     # n = [0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0769, 0.0833, 0.0909, 0.1, 0.1111, 0.125, 0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

#     ## Weighted B // 2/2, 2/3, 2/4...2/14
#     n = [0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

#     ## Starting at the 7th number
#     i = 27
#     while i < len(allData):
#       tempValues = allData[i-27:i+1]
#       ema = 0.0
#       dem = 0.0
      
#       ## Go though list and calculate the EMA for the selected seven days
#       for j, v in enumerate(tempValues):
#         if v != -1:
#           ema += (v * n[j])
#           dem += n[j]
      
#       if ema == 0:
#         # expMA.append(None)
#         expMA.append(expMA[-1])
#       else:
#         expMA.append(ema/dem)
      
#       ## Go to next 7 days
#       i += 1

#     individualAvgData[param] = {
#       "dates": allDates[27:],
#       "averages": expMA
#     }

#   return individualAvgData, processedData


# #### FUNCTION: calculates 7 DAY WEIGHTED moving average
# def sevenDayWeightedlMovingAverage(filecsv):
#   processedData = dataWithFormScore(filecsv)
#   individualAvgData = {}
 
#   ## list is already sorted, so take the first and last date of ["total"]["dates"]
#   startDate = processedData["total"]["dates"][0]
#   endDate = processedData["total"]["dates"][-1]

#   ## Get every date between start and end date
#   allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

#   for param, data in processedData.items():
#     allData = []
#     expMA = []

#     ## Fill allData -1 for any value missing user data
#     for date in allDates:
#       if (date in data["dates"]):
#         ## If date exists in the list, use the recorded data
#         idx = data["dates"].index(date)
#         allData.append(data["values"][idx])
#       else:
#         ## Put -1 as filler to filter out later
#         allData.append(-1)


#     ### Exponential
#     # n = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

#     ## Weighted A
#     # n = [0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

#     ## Weighted B
#     n = [0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

#     ## Starting at the 7th number
#     i = 6
#     while i < len(allData):
#       tempValues = allData[i-6:i+1]
#       ema = 0.0
#       dem = 0.0
      
#       ## Go though list and calculate the EMA for the selected seven days
#       for j, v in enumerate(tempValues):
#         if v != -1:
#           ema += (v * n[j])
#           dem += n[j]
      
#       if ema == 0:
#         # expMA.append(None)
#         expMA.append(expMA[-1])
#       else:
#         expMA.append(ema/dem)
      
#       ## Go to next 7 days
#       i += 1

#     individualAvgData[param] = {
#       "dates": allDates[6:],
#       "averages": expMA
#     }

#   return individualAvgData, processedData


# #### FUNCTION: calculates 7 DAY WEIGHTED moving average WITH Z-SCORE
# def sevenDayWeightedMovingAverageWithZScore(filecsv):
#   processedData, individualData = zScoreAllData(filecsv)
#   individualAvgData = {}
 
#   ## list is already sorted, so take the first and last date of ["total"]["dates"]
#   startDate = processedData["total"]["dates"][0]
#   endDate = processedData["total"]["dates"][-1]

#   ## Get every date between start and end date
#   allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

#   for param, data in processedData.items():
#     ## make two lists, one for the data in past 90 days and other for all data collected
#     allData = []
#     ninetyData = []
    
#     ## Initialize arrays for the moving average for each set of data
#     maAll = []
#     ma90 = []

#     ## Fill allData -1 for any value missing user data
#     for date in allDates:
#       if (date in data["dates"]):
#         ## If date exists in the list, use the recorded data
#         idx = data["dates"].index(date)
#         allData.append(data["zscoreAll"][idx])
#         ninetyData.append(data["zscore90"][idx])
#       else:
#         ## Put -1 as filler to filter out later
#         allData.append(-1)
#         ninetyData.append(-1)


#     ### Exponential
#     # n = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

#     ## Weighted A
#     # n = [0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

#     ## Weighted B
#     n = [0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

#     ## Starting at the 7th number
#     i = 6
#     while i < len(allData):
#       tempValuesAll = allData[i-6:i+1]
#       emaAll = 0.0
#       demAll = 0.0
      
#       ## First go though list and calculate the moving average for the selected seven days for all data
#       for j, v in enumerate(tempValuesAll):
#         if v != -1:
#           emaAll += (v * n[j])
#           demAll += n[j]
      
#       if emaAll == 0:
#         # maAll.append(None)
#         maAll.append(maAll[-1])
#       else:
#         maAll.append(emaAll/demAll)
      
#       tempValues90 = ninetyData[i-6:i+1]
#       ema90 = 0.0
#       dem90 = 0.0

#       ## Then go though list and calculate the moving average for the selected seven days for the 90 day data
#       for j, v in enumerate(tempValues90):
#         if v != -1:
#           ema90 += (v * n[j])
#           dem90 += n[j]
      
#       if ema90 == 0:
#         # ma90.append(None)
#         ma90.append(ma90[-1])
#       else:
#         ma90.append(ema90/dem90)
      
#       ## Go to next 7 days
#       i += 1

#     ## Averages using the z score
#     individualAvgData[param] = {
#       "dates": allDates[6:],
#       "averagesAll": maAll,
#       "averages90": ma90
#     }

#   return individualAvgData, processedData


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


##########################################################################################
##########################################################################################
##########################################################################################


#### FUNCTION: takes in avg intValue per param by date from csv 
#### finds the mean and std for each parameter 
def loadGPscores_oneUser(GPdata):
  
  ## empty dictionary to be filled with general pop data
  generalPopulationData = {
    "fatigue": {
      "values": [],
      "mean": 0,
      "std": 0
    },
    "soreness": {
      "values": [],
      "mean": 0,
      "std": 0
    },
    "stress": {
      "values": [],
      "mean": 0,
      "std": 0
    },
    "sleepQuality": {
      "values": [],
      "mean": 0,
      "std": 0
    },
    "sleepQuantity": {
      "values": [],
      "mean": 0,
      "std": 0
    },
    "nutrition": {
      "values": [],
      "mean": 0,
      "std": 0
    },
    "hydration": {
      "values": [],
      "mean": 0,
      "std": 0
    },
    "overall": {
      "values": [],
      "mean": 0,
      "std": 0
    }
  }

  ## Get a list of all dates
  datesRaw = []

  with open(GPdata) as generalPopData:
    csvReader = csv.reader(generalPopData)

    for row in csvReader:
      intValue = float(row[0])
      param = int(row[2])
      datesRaw.append(datetime.date.fromtimestamp(int(row[1])))
      

      ## If param is fatigue, stress or soreness we subtract from 5 to get the score
      if param == 492:
        generalPopulationData["fatigue"]["values"].append((6 - intValue) * 20)
      
      if param == 493:
        generalPopulationData["soreness"]["values"].append((6 - intValue) * 20)

      if param == 494:
        generalPopulationData["stress"]["values"].append((6 - intValue) * 20)

      ## Other params just go to a 100 pt scale
      if param == 495:
        generalPopulationData["sleepQuality"]["values"].append(intValue * 20)
      
      if param == 496:
        generalPopulationData["nutrition"]["values"].append(intValue * 20)

      if param == 497:
        generalPopulationData["hydration"]["values"].append(intValue * 20)

      if param == 498:
        generalPopulationData["overall"]["values"].append(intValue * 20)

      ## Map the hours of sleep to score for the total score calculation
      if param == 614:
        if (intValue >= 9):
          generalPopulationData["sleepQuantity"]["values"].append(100)
        elif (intValue >= 8 and intValue < 9):
          generalPopulationData["sleepQuantity"]["values"].append(90)
        elif (intValue >= 7 and intValue < 8):
          generalPopulationData["sleepQuantity"]["values"].append(80)
        elif (intValue >= 6 and intValue < 7):
          generalPopulationData["sleepQuantity"]["values"].append(70)
        elif (intValue >= 5 and intValue < 6):
          generalPopulationData["sleepQuantity"]["values"].append(55)
        elif (intValue >= 4 and intValue < 5):
          generalPopulationData["sleepQuantity"]["values"].append(40)
        else:
          generalPopulationData["sleepQuantity"]["values"].append(0)
    
  ## Go through the object we just created and find the mean and std with numpy
  for param, data in generalPopulationData.items():

    generalPopulationData[param]["mean"] = np.mean(generalPopulationData[param]["values"])
    generalPopulationData[param]["std"] = np.std(generalPopulationData[param]["values"])

    ## Remove the values list, not necessary to pass through and its very long
    del generalPopulationData[param]["values"]


  datesUniqueSet = sorted(list(set(datesRaw)))

  ## Get total score, pass in all unique dates and csv again
  totalScoreData = getTotalScorePerDate(datesUniqueSet, GPdata)

  generalPopulationData["total"] = {
    # "values": totalScoreData["totalScore"],
    "mean": np.mean(totalScoreData["totalScore"]),
    "std": np.std(totalScoreData["totalScore"])
  }

  return generalPopulationData


#### FUNCTION: calculates form score out of 100 pt scale
#### Includes hours of sleep
def getTotalScorePerDate(dates, filecsv):

  totalScoreData = {
    "dates": dates,
    "sum": [0] * len(dates),
    "count": [0] * len(dates),
    "totalScore": []
  }

  with open(filecsv) as generalPopData:
    csvReader = csv.reader(generalPopData)

    for row in csvReader:
      intValue = float(row[0])
      param = int(row[2])
      date = datetime.date.fromtimestamp(int(row[1]))

      ## Find index of date in list of unique dates
      idx = totalScoreData["dates"].index(date)

      ## If param is fatigue, stress or soreness we subtract from 5 to get the score then go to 100 pt scale
      if ((param == 492) or (param == 493) or (param == 494)):
        totalScoreData["sum"][idx] += ((5 - intValue) * 20)
        ## Add 100 for total possible points for each score added
        totalScoreData["count"][idx] += 100
      
      ## Other params just go to a 100 pt scale
      elif ((param == 495) or (param == 496) or (param == 497) or (param == 498)):
        totalScoreData["sum"][idx] += (intValue * 20)
        ## Add 100 for total possible points for each score added
        totalScoreData["count"][idx] += 100

      ## Map the hours of sleep to score for the total score calculation
      elif (param == 614):
        if (intValue >= 9):
          totalScoreData["sum"][idx] += (100)
          totalScoreData["count"][idx] += 100
        elif (intValue >= 8 and intValue < 9):
          totalScoreData["sum"][idx] += (90)
          totalScoreData["count"][idx] += 100
        elif (intValue >= 7 and intValue < 8):
          totalScoreData["sum"][idx] += (80)
          totalScoreData["count"][idx] += 100
        elif (intValue >= 6 and intValue < 7):
          totalScoreData["sum"][idx] += (70)
          totalScoreData["count"][idx] += 100
        elif (intValue >= 5 and intValue < 6):
          totalScoreData["sum"][idx] += (55)
          totalScoreData["count"][idx] += 100
        elif (intValue >= 4 and intValue < 5):
          totalScoreData["sum"][idx] += (40)
          totalScoreData["count"][idx] += 100
        else:
          totalScoreData["count"][idx] += 100

  ## Go through the data and calculate form score per day out of 100
  for i, s in enumerate(totalScoreData["sum"]):
    totalScoreData["totalScore"].append((s*100)/(totalScoreData["count"][i]))

  return totalScoreData


# #### FUNCITON: calculates the zscore for each parameter 
# #### using the personal history (PH)
# def zScorePH90Days(filecsv, filecsvGP):
#   processedData = dataWithFormScore(filecsv)

#   generalPopulationData = loadGPscores_oneUser(filecsvGP)
  
#   ## Initialize object to return with all data points
#   individualAvgData = {}
 
#   for param, data in processedData.items():

#     ## Initialize the lists to hold personal history data
#     meanPH = []
#     stdPH = []

#     ## Get the 90th day for the boundary condition
#     day90 = (data["dates"][0] + datetime.timedelta(days = 90))

#     for i,d in enumerate(data["dates"]):
      
#       ## For each date, get the mean and std for the past 90 days
#       ninetyDaysAgo = (d - datetime.timedelta(days = 90))
#       ninetyDayData = []
      
#       ## Go through dates again to find the values in past 90 days
#       for j, innerDate in enumerate(data["dates"]):
#         if ((innerDate <= d) and (innerDate > ninetyDaysAgo)):

#           ## Add the value to the 90 day list
#           ninetyDayData.append(data["values"][j])


#       ## If we don't have 10 data points and we are in the first 90 days 
#       ## use the GP mean for this param for calculating mean and std
#       if ((len(ninetyDayData) < 10) and (d <= day90)):
#         i = 0
#         weightedGeneralPop = (10 - len(ninetyDayData))
#         while (i < weightedGeneralPop):
#           ## Add the general population mean to the list to calculate the mean and std
#           ninetyDayData.append(generalPopulationData[param]["mean"])
#           i += 1

#       ## If we don't have 10 data points and we past the first 90 days, 
#       ## go back to collect data in past until we have 10 data points
#       elif ((len(ninetyDayData) < 10) and (d > day90)):
#         daysBack = 1
#         while (len(ninetyDayData) < 10):
          
#           ## Make sure we don't index before beginning of list
#           if (i - daysBack > 0):
#             ninetyDayData.append(data["values"][i - daysBack])
#             daysBack += 1
          
#           ## Have to add the general population mean if not enough data
#           else:
#             ninetyDayData.append(generalPopulationData[param]["mean"])

#       ## Get the mean and standard deviation using data from past 90 days
#       meanPH.append(np.mean(ninetyDayData))
#       stdPH.append(np.std(ninetyDayData))

#     individualAvgData[param] = {
#       "dates": data["dates"],
#       "values": data["values"],
#       "meanPH": meanPH,
#       "stdPH": stdPH
#     }

#   # Add z-score for the 90 day avg and std
#   for param, data in individualAvgData.items():
    
#     ## Initialize the z-score list 
#     zscoreData = []

#     for i, d in enumerate(data["dates"]):
#       if data["stdPH"][i] == 0:
#         zscoreData.append(0)
#       else: 
#         zscore = (data["values"][i] - data["meanPH"][i]) / data["stdPH"][i]
#         zscoreData.append(zscore)

#     ## Add z-score to the data in the object to return
#     individualAvgData[param]["zscorePH"] = zscoreData

#   ## Returns object of parameters with dates, score values, means, stds, and z-scores using the 90 day personal history
#   return individualAvgData, generalPopulationData


#### FUNCITON: calculates the zscore for each parameter 
#### using the personal history of the last 20 collected data points (PH)
def zScorePH20Points(filecsv, filecsvGP):
  processedData = dataWithFormScore(filecsv)

  generalPopulationData = loadGPscores_oneUser(filecsvGP)
  
  ## Initialize object to return with all data points
  individualAvgData = {}
 
  for param, data in processedData.items():

    ## Initialize the lists to hold personal history data
    meanPH = []
    stdPH = []

    for i,d in enumerate(data["dates"]):
      temp20PointData = []
       
      ## Less than 20 data points so we need to add the general population
      if i < 20:
        temp20PointData = data["values"][0:i+1]
        while (len(temp20PointData) < 20):
          ## Fill with the general pop avg data point
          temp20PointData.append(generalPopulationData[param]["mean"])
      else:
        temp20PointData = data["values"][i-19:i+1]

      ## Get the mean and standard deviation using data from past 20 data points
      meanPH.append(np.mean(temp20PointData))
      stdPH.append(np.std(temp20PointData))

    individualAvgData[param] = {
      "dates": data["dates"],
      "values": data["values"],
      "meanPH": meanPH,
      "stdPH": stdPH
    }

  # # Add z-score for the 90 day avg and std
  # for param, data in individualAvgData.items():
    
  #   ## Initialize the z-score list 
  #   zscoreData = []

  #   for i, d in enumerate(data["dates"]):
  #     if data["stdPH"][i] == 0:
  #       zscoreData.append(0)
  #     else: 
  #       zscore = (data["values"][i] - data["meanPH"][i]) / data["stdPH"][i]
  #       zscoreData.append(zscore)

  #   ## Add z-score to the data in the object to return
  #   individualAvgData[param]["zscorePH"] = zscoreData

  ## Returns object of parameters with dates, score values, means and stds using the 90 day personal history
  return individualAvgData, generalPopulationData


#### FUNCITON: calculates the zscore for each parameter 
#### using the general population data (GP)
def zScoreAllDataGP(filecsv, filecsvGP):

  ## Already have the PH data from this function
  # individualAvgData, generalPopulationData = zScorePH90Days(filecsv, filecsvGP)
  individualAvgData, generalPopulationData = zScorePH20Points(filecsv, filecsvGP)

  # Add z-score for all data avg and std
  for param, data in individualAvgData.items():

    zscoreDataTemp = []
  
    for i, d in enumerate(data["dates"]):

      ## Calculate the score for each date using the general population data
      zscore = (data["values"][i] - generalPopulationData[param]["mean"]) / generalPopulationData[param]["std"]
      zscoreDataTemp.append(zscore)

    ## Add the z-score for general population data
    individualAvgData[param]["zscoreGP"] = zscoreDataTemp

  return individualAvgData


#### FUNCTION: calculates the 14 day weighted moving average of the z-score using the PH data
def fourteenDayWeightedMovingAverageZScorePH(filecsv, filecsvGP):
  ## Get the z-score data for PH and GP, just configuring the PH moving avg here
  individualAvgData = zScoreAllDataGP(filecsv, filecsvGP)

  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = individualAvgData["total"]["dates"][0]
  endDate = individualAvgData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in individualAvgData.items():
    ## Initialize the list to hold the temp data 
    tempData = []
    
    ## Fill with -1 for any value missing recorded user data
    for d in allDates:
      ## If date exists in the parameter's date list, use the recorded data
      if (d in data["dates"]):
        idx = data["dates"].index(d)
        tempData.append(data["meanPH"][idx])
      else:
        ## Put -1 as filler to filter out later
        tempData.append(-1)

    ## Weighted B
    n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    ## Initialize array to hold moving average for all dates
    tempMovingAverages = []

    i = 0
    while i < len(tempData):
      tempValuesAll = []
      if i < 13:
        tempValuesAll = tempData[0:i+1]
      else:
        tempValuesAll = tempData[i-13:i+1]
      weightedSum = 0.0
      totalCoefficient = 0.0

      ## Go though list and calculate the moving average for the selected fourteen days for all data
      for j, v in enumerate(tempValuesAll):
        if v != -1:
          weightedSum += (v * n[j])
          totalCoefficient += n[j]
      
      if weightedSum == 0:
        ## First value in array, cannot get previous value and all values are 0
        if i < 13:
          tempMovingAverages.append(0)
        else:
          tempMovingAverages.append(tempMovingAverages[-1])
      else:
        tempMovingAverages.append(weightedSum/totalCoefficient)
    
      ## Go to next 14 days
      i += 1

    ## Go through the 14 day moving average and select the days that had user input
    filteredData = []
    zscoreData = []

    for k, userDate in enumerate(data["dates"]):
      dateIndex = allDates.index(userDate)
      meanData = tempMovingAverages[dateIndex]
      filteredData.append(meanData)
        
      if data["stdPH"][k] == 0:
        zscoreData.append(0)
      else: 
        zscore = (data["values"][k] - meanData) / data["stdPH"][k]
        zscoreData.append(zscore)

    ## Add weighted moving average and zscore data using personal history data
    individualAvgData[param]["weightedDates"] = data["dates"][7:]
    individualAvgData[param]["weightedMovingAveragePH"] = filteredData[7:]
    individualAvgData[param]["weightedMovingAverageZscorePH"] = zscoreData[7:]

  return individualAvgData


#### FUNCTION: calculates the 14 day weighted moving average of the z-score using the GP data
def fourteenDayWeightedMovingAverageZScoreGP(filecsv, filecsvGP):
  ## Get the z-score data for PH and GP, just configuring the PH moving avg here
  individualAvgData = fourteenDayWeightedMovingAverageZScorePH(filecsv, filecsvGP)

  ## list is already sorted, so take the first and last date of ["total"]["dates"]
  startDate = individualAvgData["total"]["dates"][0]
  endDate = individualAvgData["total"]["dates"][-1]

  ## Get every date between start and end date
  allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  for param, data in individualAvgData.items():
    ## Initialize the list to hold the z-score
    tempData = []
    
    ## Initialize array
    tempMovingAverages = []

    ## Fill with -1 for any value missing recorded user data
    for date in allDates:
      ## If date exists in the parameter's date list, use the recorded data
      if (date in data["dates"]):
        idx = data["dates"].index(date)
        tempData.append(data["zscoreGP"][idx])
      else:
        ## Put -1 as filler to filter out later
        tempData.append(-1)

    ## Weighted B
    n = [0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

    i = 0
    while i < len(tempData):
      tempValuesAll = []
      if i < 13:
        tempValuesAll = tempData[0:i+1]
      else:
        tempValuesAll = tempData[i-13:i+1]

      weightedSum = 0.0
      totalCoefficient = 0.0
      
      ## First go though list and calculate the moving average for the selected seven days for all data
      for j, v in enumerate(tempValuesAll):
        if v != -1:
          weightedSum += (v * n[j])
          totalCoefficient += n[j]
      
      if weightedSum == 0:
        ## First value in array, cannot get previous value and all values are 0
        if i < 13:
          tempMovingAverages.append(0)
        else:
          tempMovingAverages.append(tempMovingAverages[-1])
      else:
        tempMovingAverages.append(weightedSum/totalCoefficient)
      
      ## Go to next 14 days
      i += 1

    filteredData = []

    for userDate in data["dates"]:
      dateIndex = allDates.index(userDate)
      filteredData.append(tempMovingAverages[dateIndex])
     
    ## Add averages using the z score from general population data
    individualAvgData[param]["weightedMovingAverageZscoreGP"] = filteredData[7:]

  return individualAvgData


#### FUNCTION: calculate bridge score for each parameter and total score (personal history only)
def calculatePersonalHistoryBridgeScore(filecsv, filecsvGP):
  ## Returns object with: dates, scores, meanPH, stdPh, meanGP, stdGP, zscorePH, datesMovingAveragePH, weightedMovingAveragePH, 
  ## zscoreGP, datesMovingAverageGP, weightedMovingAverageGP
  individualData = fourteenDayWeightedMovingAverageZScoreGP(filecsv, filecsvGP)

  for param, data in individualData.items():
    ## Approximating e = 2.718281
    bridgeScorePersonalHistory = [((4/(4+((np.power([2.718281], [-x]))[0]))) * 100) for x in data["weightedMovingAverageZscorePH"]]

    individualData[param]["bridgeScorePH"] = bridgeScorePersonalHistory

  return individualData


#### FUNCTION: calculate bridge score for each parameter and total score
def calculateGeneralPopulationBridgeScore(filecsv, filecsvGP):
  ## Returns object with: dates, scores, meanPH, stdPh, meanGP, stdGP, zscorePH, datesMovingAveragePH, weightedMovingAveragePH, 
  ## zscoreGP, datesMovingAverageGP, weightedMovingAverageGP and bridgeScorePH
  individualData = calculatePersonalHistoryBridgeScore(filecsv, filecsvGP)

  for param, data in individualData.items():
    bridgeScorePersonalHistory = [((4/(4+((np.power([2.718281], [-x]))[0]))) * 100) for x in data["weightedMovingAverageZscoreGP"]]

    individualData[param]["bridgeScoreGP"] = bridgeScorePersonalHistory

  return individualData


#### FUNCTION: user personal history score and general populations score for bridge score for one user
def calculateBridgeScore(filecsv, filecsvGP):
  individualData = calculateGeneralPopulationBridgeScore(filecsv, filecsvGP)

  for param, data in individualData.items():
    dataBridgeScore = []

    ## Can assume that the date exists in general population because this user is in the general population
    for i, d in enumerate(data["weightedDates"]):
      dataBridgeScore.append((0.67*(data["bridgeScorePH"][i])) + (0.33*(data["bridgeScoreGP"][i])))
    
    individualData[param]["bridgeScore"] = dataBridgeScore

  return individualData


#### FUNCTION: create table of scores for each parameter
def tableBridgeScores(filecsv, filecsvGP):
  bridgeScoreData = calculateBridgeScore(filecsv, filecsvGP)

  finalCSVData = {}

  ## Get list of all dates for bridge scores
  datesRaw = []
  for param, data in bridgeScoreData.items():
    finalCSVData[param] = []
    datesRaw += data["weightedDates"]

  ## List of dates for every piece of data 
  finalCSVData["dates"] = sorted(list(set(datesRaw)))

  for i, d in enumerate(finalCSVData["dates"]):

    ## Go through each param and construct list of values that match the dates
    for param, data in bridgeScoreData.items():
      if d in data["weightedDates"]:
        didx = data["weightedDates"].index(d)
        finalCSVData[param].append(data["bridgeScore"][didx])
      else:
        finalCSVData[param].append(-1)

  with open('8158_bridge_score_data.csv', 'wb') as bridgeScoreTable:
    writer = csv.writer(bridgeScoreTable)
    dates = copy.deepcopy(finalCSVData["dates"])
    
    ## want first cell to be empty so just add today's date
    dates.insert(0, datetime.datetime.now())
    writer.writerow([datetime.date.isoformat(d) for d in dates])

    for param, data in finalCSVData.items():
      scoreData = copy.deepcopy(data)
      scoreData.insert(int(0), param)
      writer.writerow([(round((x*1.0),4)) if (isinstance(x, float) or isinstance(x, int)) else x for x in scoreData])


#### FUNCTION: show bridge score for all parameters and total score over time (personal history only)
def graphBridgeScore(filecsv):
  bridgeScoreData = calculateBridgeScore(filecsv)

  fig, ax = plt.subplots()
  graphTitle = "Total - Scores"

  # values = bridgeScoreData["overall"]["bridgeScore"][89:]
  # dates = bridgeScoreData["overall"]["datesMovingAveragePH"][89:]
  # ax.plot(dates, values, label="Overall")

  # values2 = bridgeScoreData["total"]["bridgeScore"][89:]
  # dates2 = bridgeScoreData["total"]["datesMovingAveragePH"][89:]
  # ax.plot(dates2, values2, label="Total")


  values = bridgeScoreData["total"]["bridgeScorePH"][89:]
  dates = bridgeScoreData["total"]["datesMovingAveragePH"][89:]
  ax.plot(dates, values, label="PH Score")

  values2 = bridgeScoreData["total"]["bridgeScoreGP"][89:]
  dates2 = bridgeScoreData["total"]["datesMovingAveragePH"][89:]
  ax.plot(dates2, values2, label="GP Score")

  values3 = bridgeScoreData["total"]["bridgeScore"][89:]
  dates3 = bridgeScoreData["total"]["datesMovingAveragePH"][89:]
  ax.plot(dates3, values3, label="Bridge Score")


  # for param, data in bridgeScoreData.items():
  #   values = bridgeScoreData[param]["bridgeScore"][89:]
  #   dates = bridgeScoreData[param]["datesMovingAveragePH"][89:]
  #   ax.plot(dates, values, label=param)

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





















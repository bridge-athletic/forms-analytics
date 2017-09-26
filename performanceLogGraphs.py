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
        ## calculate score for sleep
        score = ((5 - int(row[3])) + 1)
        individualPerformanceLogScores["stress"]["values"].append(int(row[3]))
      
      ## sleep data; parameterId 495
      if (int(row[1]) == 495):
        individualPerformanceLogScores["sleep"]["dates"].append(date)
        individualPerformanceLogScores["sleep"]["values"].append(int(row[3]))
      
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
  graphTitle = "Number of Questions Answered per Form Submission (max. 7)"
  ax.plot(dates, numResponses, label='Num. Questions Answered')

  ax.grid(True)
  ax.set_ylim(0, 7.5)
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
  print k

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
    # n = [0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

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
def dataStandardDeviationWithFormScore(filecsv):
  processedData = dataWithFormScore(filecsv)
  individualAvgData = {}
 
  for param, data in processedData.items():
    meanData = []
    stdData = []

    for i, d in enumerate(data["dates"]):
      
      ## For each date, get the mean and std for the past 90 days
      nintyDaysAgo = (d - datetime.timedelta(days = 90))
      nintyDayData = []
      
      ## Go through dates again to find the values in past 90 days
      for innerDate in data["dates"]:
        if ((innerDate < d) and (innerDate > nintyDaysAgo)):

          ## Add the value to the temp list
          nintyDayData.append(data["values"][i])

      meanData.append(np.mean(nintyDayData))
      stdData.append(np.std(nintyDayData))

    individualAvgData[param] = {
      "dates": data["dates"],
      "values": data["values"],
      "means": meanData,
      "std": stdData
    }

  # print len(data["dates"])
  # print len(data["values"])
  # print len(meanData)
  # print len(stdData)

  ## Add z-score
  # for param, data in individualAvgData.items():
  #   zscoreData = []

  #   for i, d in enumerate(data["dates"]):

  #     zscore = (data["values"][i] - 


  return individualAvgData, processedData


  # ## list is already sorted, so take the first and last date of ["total"]["dates"]
  # startDate = processedData["total"]["dates"][0]
  # endDate = processedData["total"]["dates"][-1]

  # ## Get every date between start and end date
  # allDates = [startDate + datetime.timedelta(days = x) for x in range((endDate - startDate).days + 1)]

  # for param, data in processedData.items():
  #   allData = []
  #   means = []

  #   ## Fill allData -1 for any value missing user data
  #   for date in allDates:
  #     if (date in data["dates"]):
  #       ## If date exists in the list, use the recorded data
  #       idx = data["dates"].index(date)
  #       allData.append(data["values"][idx])
  #     else:
  #       ## Put -1 as filler to filter out later
  #       allData.append(-1)


  #   ### Exponential
  #   # n = [ 0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1]

  #   ## Weighted A // 1/2, 1/3...1/14
  #   # n = [0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0714, 0.0769, 0.0833, 0.0909, 0.1, 0.1111, 0.125, 0.1429, 0.1667, 0.2, 0.25, 0.3333, 0.5, 1]

  #   ## Weighted B // 2/2, 2/3, 2/4...2/14
  #   # n = [0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1538, 0.1667, 0.1818, 0.2, 0.2222, 0.25, 0.2857, 0.3333, 0.4, 0.5, 0.6667, 1]

  #   ## Starting at the 90th date and get the last 90 day average for each day
  #   i = 90
  #   while i < len(allData):
  #     tempValues = allData[i-89:i+1]
  #     total = 0.0
  #     dem = 0.0
      
  #     ## Go though list and calculate the average for the last 90 days
  #     for j, v in enumerate(tempValues):
  #       if v != -1:
  #         total += v
  #         dem += 1
      
  #     if total == 0:
  #       # means.append(None)
  #       means.append(means[-1])
  #     else:
  #       means.append(total/dem)
      
  #     ## Go to next 90 days
  #     i += 1

  #   individualAvgData[param] = {
  #     "dates": allDates[89:],
  #     "values": data["values"][89:],
  #     "averages": means
  #   }

  #   ## now we can get the std for each day 
  #   ## need to do this manually since so much of the data is missing and needed to calculate mean 
  #   for param, data in individualAvgData.items():
  #     std = []
      
  #     ## Go through the values and calculate the std for each corresponding day
  #     for k, x in enumerate(data["values"]):
  #       if x != -1:
  #         tempStd = (x - data["averages"][k])/



  # return individualAvgData, processedData

#### FUNCTION: takes moving average data and plots it with the form score
def showMovingAverageAndTotalScore(filecsv, parameter):

  #### This is for 7 POINT moving average
  # avgData, processedData = sevenPointMovingAverage(filecsv)
  # graphTitle = "Individual 7 Point Moving Average"
  # filename = "_7PT_Moving_Average.png"
  
  #### This is for 7 DAY moving average
  # avgData, processedData = sevenDayMovingAverage(filecsv)
  # graphTitle = "Individual 7 Day Moving Average"
  # filename = "_7DAY_Moving_Average.png"

  #### This is for 7 POINT EXPONENTIAL moving average
  # avgData, processedData = sevenPointExponentialMovingAverage(filecsv)
  # graphTitle = "Individual 7 Point Exponential Moving Average"
  # filename = "_7PT_Exponential_Moving_Average.png"

  #### This is for 7 POINT WEIGHTED moving average
  # avgData, processedData = sevenPointWeightedMovingAverage(filecsv)
  # graphTitle = "Individual 7 Point Weighted Moving Average"
  # filename = "_7PT_Weighted_Moving_Average_OTHER.png"

  #### This is for 7 DAY EXPONENTIAL moving average
  # avgData, processedData = sevenDayExponentialMovingAverage(filecsv)
  # graphTitle = "Individual 7 Day Exponential Moving Average"
  # filename = "_7DAY_Exponential_Moving_Average.png"

  #### This is for 7 DAY EXPONENTIAL moving average
  avgData, processedData = twentyEightDayExponentialMovingAverage(filecsv)
  graphTitle = "Individual 28 Day Moving Moving Average"
  filename = "_28DAY_Moving_Moving_Average.png"


  ## initialize the plot
  fig, ax = plt.subplots()

  if (parameter == 'fatigue'):
    ## update data so its out of 100
    values = [((v*100)/5) for v in avgData["fatigue"]["averages"]]
    dates = avgData["fatigue"]["dates"]
    ax.plot(dates, values, label='Fatigue')
    # graphTitle += 'Fatigue '

  elif (parameter == 'soreness'):
    dates = avgData["soreness"]["dates"]
    values = [((v*100)/5) for v in avgData["soreness"]["averages"]]
    ax.plot(dates, values, label='Soreness')
    # graphTitle += 'Soreness '

  elif (parameter == 'stress'):
    dates = avgData["stress"]["dates"]
    values = [((v*100)/5) for v in avgData["stress"]["averages"]]
    ax.plot(dates, values, label='Stress')
    # graphTitle += 'Stress '

  elif (parameter == 'sleep'):
    dates = avgData["sleep"]["dates"]
    values = [((v*100)/5) for v in avgData["sleep"]["averages"]]
    ax.plot(dates, values, label='Sleep')
    # graphTitle += 'Sleep '

  elif (parameter == 'hydration'):
    dates = avgData["hydration"]["dates"]
    values = [((v*100)/5) for v in avgData["hydration"]["averages"]]
    ax.plot(dates, values, label='Hydration')
    # graphTitle += 'Hydration '

  elif (parameter == 'nutrition'):
    dates = avgData["nutrition"]["dates"]
    values = [((v*100)/5) for v in avgData["nutrition"]["averages"]]
    ax.plot(dates, values, label='Nutrition')
    # graphTitle += 'Nutrition '

  elif (parameter == 'overall'):
    dates = avgData["overall"]["dates"]
    values = [((v*100)/5) for v in avgData["overall"]["averages"]]
    ax.plot(dates, values, label='Overall')
    # graphTitle += 'Overall '

  ## Add the total form score 
  totalDates = avgData["total"]["dates"]
  totalValues = avgData["total"]["averages"]
  ax.plot(totalDates, totalValues, label='Total Score')
  # graphTitle += 'with Total Score '

  ax.grid(True)
  ax.set_ylim(0, 105)
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  fig.autofmt_xdate()
  ax.legend(loc=3)

  ## set axes and title
  ax.set_xlabel('Dates')
  ax.set_ylabel('Values')
  ax.set_title(graphTitle)
  
  # plt.savefig(parameter + filename)
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
  
  plt.savefig(parameter + "_with_form_score.png")
  plt.show()
















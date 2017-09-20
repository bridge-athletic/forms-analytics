#### Importing functions to load data related to the performance log
import performanceLogGraphs as plog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#### Specify the parameters for trends
#### Options are: fatigue, soreness, sleep, stress, nutrition, hydration and overall

# params = "sleep, overall"


#### Specify the csv file 
#### CSV file must be raw data only, csv in following format:
#### userId, parameterId, UNIX timestamp, value
filecsv = 'Individual_performance_log_data.csv'
# userId = 4349



#### Print data
# print "Processed Performance Log Data for " + userId
# print individual_data

#### Show trends of specified params
# plog.individualParamTrend(filecsv, params)

#### Show trend of form score // requires in processed data
# plog.requestIndividualFormScore(individual_data)

#### Show raw data vs mean / max data before processed
# plog.showRawMeanMax(filecsv)

#### Show parameter on scale of 100 with form score
# param = "fatigue"
# plog.graphParamAndFormScore(filecsv, param)


#### Calculate moving averages for each parameter
param = "fatigue"
plog.showMovingAverageAndTotalScore(filecsv, param)



# TODOs

# 0) Generate data (follows the same structure as dataRaw but post-mean processing)
# 1) Add to data['total']['values'] and data['total']['dates']
# ---  sorted(list(set(data['nutrition']['dates']+data['sleep']['dates'])))
# 2) Nice plot of each category vs. time, with total overlayed (8 figures)
# 3) Nice plot of 7pt-Moving-average of each category vs. time, with total overlayed (8 figures)
# 4) Nice plot of 7Day-Moving-average of each category vs. time, with total overlayed (8 figures)


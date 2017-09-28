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


#### Shows number of questions answered per submission
# plog.questionsAnsweredPerSubmission(filecsv)


#### Show parameter on scale of 100 with form score
# param = "overall"
# plog.graphParamAndFormScore(filecsv, param)


#### Calculate 7 point moving averages for every parameter
# param = "fatigue"
# plog.dataPointMovingAverage(filecsv)


#### Show moving averages (7 point or 7 day) for one parameter with total score
# param = "overall"
# plog.showMovingAverageAndTotalScore(filecsv, param)


#### Show z score for each category with total z score
param = "overall"
plog.showZscore90DaysVsAllData(filecsv, param)

#### Show scatterplot for correlation
# param1 = "fatigue"
# param2 = "nutrition"
# plog.graphScatterPlot(filecsv, param1, param2)





# TODOs
## add weighted t the title 
## label the z score

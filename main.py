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
# filecsv = '12377_performance_log_data.csv'
filecsv = '12379_performance_log_data.csv'
# filecsv = '12426_performance_log_data.csv'
# filecsv = '17822_performance_log_data.csv'
# filecsv = '18276_performance_log_data.csv'
# filecsv = '4349_performance_log_data.csv'
# filecsv = '5584_performance_log_data.csv'
# filecsv = '8117_performance_log_data.csv'
# filecsv = '8155_performance_log_data.csv'
# filecsv = '8158_performance_log_data.csv'











filecsvGP = 'GP_param_intValue_by_date.csv'

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
# param = "sleepQuantity"
# plog.showMovingAverageAndTotalScore(filecsv, param)


#### Show z score for each category with total z score
# param = "sleepQuantity"
# plog.showZscore90DaysVsAllData(filecsv, param)


#### Show z score for each category with total z score
# param = "overall"
# plog.createScatterPlotDF(filecsv)


#### Show scatterplot
# param = "total"
# plog.correlationCoeffiecent(filecsv, param)
# sleepQuantity
# sleepQuality

#### Show scatterplot
# param1 = "stress"
# param2 = "overall"
# plog.graphScatterPlot(filecsv, param1, param2)


#### Show trends for bridge score (personal history only)
# plog.graphBridgeScorePH(filecsv)


# plog.calculateBridgeScore(filecsv)

plog.tableBridgeScores(filecsv, filecsvGP)
# plog.graphBridgeScore(filecsv)


#### data with form score and sleep quantity
# plog.loadGPscores_oneUser('GP_param_intValue_by_date.csv')




























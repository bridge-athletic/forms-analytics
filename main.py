#### Importing functions to load data related to the performance log
import performanceLogGraphs as plog


#### Specify the parameters for trends
#### Options are: fatigue, soreness, sleep, stress, nutrition, hydration and overall
params = "sleep, overall"


#### Specify the csv file 
#### CSV file must be raw data only, csv in following format:
#### userId, parameterId, UNIX timestamp, value
data_file = 'Individual_performance_log_data.csv'
userId = 4349


#### Load data from csv file 
individual_data = plog.loadData_oneUser(data_file)

#### Print data
# print "Processed Performance Log Data for " + userId
# print individual_data


#### Show trends of specified params
# plog.requestIndividualParamTrend(individual_data, params)


#### Show trend of form score // requires in processed data
plog.requestIndividualFormScore(individual_data)




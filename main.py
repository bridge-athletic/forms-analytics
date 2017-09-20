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


#### Load data from csv file 
dataRaw = plog.loadData_oneUser(filecsv)

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

# print datesUnique
# print valuesUniqueMean

#### Plotting data
fig, ax = plt.subplots()
ax.plot(datesUnique, valuesUniqueMean, label='Unique Mean')
ax.plot(datesUnique, valuesUniqueMax, label='Unique Max')
ax.plot(datesRaw, valuesRaw, label='Raw Data')
ax.grid(True)
# ax.set_ylim(0, 38)
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
fig.autofmt_xdate()
ax.legend(loc=4)
## set axes and title
ax.set_xlabel('Dates')
ax.set_ylabel(parameterName)
ax.set_title(parameterName)
plt.show()


#### Print data
# print "Processed Performance Log Data for " + userId
# print individual_data

#### Show trends of specified params
# plog.requestIndividualParamTrend(individual_data, params)

#### Show trend of form score // requires in processed data
# plog.requestIndividualFormScore(individual_data)


# TODOs

# 0) Generate data (follows the same structure as dataRaw but post-mean processing)
# 1) Add to data['total']['values'] and data['total']['dates']
# ---  sorted(list(set(data['nutrition']['dates']+data['sleep']['dates'])))
# 2) Nice plot of each category vs. time, with total overlayed (8 figures)
# 3) Nice plot of 7pt-Moving-average of each category vs. time, with total overlayed (8 figures)
# 4) Nice plot of 7Day-Moving-average of each category vs. time, with total overlayed (8 figures)


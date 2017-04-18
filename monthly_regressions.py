#################################################
##################### USAGE #####################
"""
Change variables in script then from command
line, run the command:
$ python monthly_regressions.py station.csv yearstart yearend
"""
#################################################
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import calendar
from scipy.optimize import leastsq
import data_utils as du
import pandas as pd
import time
import sys

start = time.time()
print('Reading CSVs')

station_csv, yearstart, yearend = sys.argv[-3:]

#### dataframes ####
df = pd.read_csv(station_csv, parse_dates=True)

years = df.get('Year').as_matrix()
MSL = df.get(' MSL').as_matrix()

years = years.astype('int')
MSL = MSL.astype('float')

indices = np.where((years >= int(yearstart)) & (years <= int(yearend)))[0]

years, MSL = years[indices[0]:indices[-1]], MSL[indices[0]:indices[-1]]


# #### Slope Lines ####
A = np.vstack([years, np.ones(len(years))]).T
m_sea_level, b_sea_level = np.linalg.lstsq(A, MSL)[0]
print('slope for water level data set = ', m_sea_level)
print('suppressing notation = {0:.20f}'.format(m_sea_level))
mx_plus_b = m_sea_level * years + b_sea_level

memory = 12
ROC = (mx_plus_b[-1] - mx_plus_b[0]) / mx_plus_b[0]
print("ROC: {}".format(ROC))
print("Slope: {}".format(m_sea_level))

##########################################################################################
######################################## Graphing ########################################
##########################################################################################
# print('graphing, {}'.format(time.time() - start))
# plt.rcParams['agg.path.chunksize'] = 100000
# # plt.style.use('ggplot')
# fig = plt.figure(figsize=(20, 10))

# # water level
# ax = fig.add_subplot(111)
# ax.plot(years, MSL, color='red')
# ax.plot(years, m_sea_level * years + b_sea_level, color='black')
# plt.show()

#################################################
##################### USAGE #####################
"""
Change variables in script then from command
line, run the command:
$ python run_regressions.py station.csv yearstart yearend
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
station = pd.read_csv(station_csv, parse_dates=True)

t_datetime, pressure, t_timestamp, water_level = [station.as_matrix()[:,n] for n in range(1,5)]
t_datetime = np.array(list(map(lambda s: dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S'), t_datetime)))
year_index = np.array([x.year for x in t_datetime])

indices = np.where((year_index >= int(yearstart)) & (year_index <= int(yearend)))[0]

t_datetime, t_timestamp, water_level = t_datetime[indices[0]:indices[-1]], t_timestamp[indices[0]:indices[-1]], water_level[indices[0]:indices[-1]]

water_level = water_level.astype('float')
pressure = pressure.astype('float')
water_level = water_level.astype('float')

#### Slope Lines ####
A = np.vstack([t_timestamp, np.ones(len(t_timestamp))]).T
m_water_level, b_water_level = np.linalg.lstsq(A, water_level)[0]
print('slope for water level data set = ', m_water_level)
print('suppressing notation = {0:.20f}'.format(m_water_level))
memory = 200
print('Difference in Epoch = {}'.format(np.mean(water_level[-200:] - np.mean(water_level[:200]))))

##########################################################################################
######################################## Graphing ########################################
##########################################################################################
# print('graphing, {}'.format(time.time() - start))
# autoTicks = mdates.AutoDateLocator()
# autoFmt = mdates.AutoDateFormatter(autoTicks)
# plt.rcParams['agg.path.chunksize'] = 100000
# fig = plt.figure(figsize=(20, 10))

# # water level
# ax = fig.add_subplot(111)
# ax.plot(mdates.date2num(t_datetime), water_level, color='orange')
# ax.plot(mdates.date2num(t_datetime), m_water_level * t_timestamp + b_water_level, 'blue')
# ax.set_ylabel('Water Level')
# ax.xaxis.set_major_locator(autoTicks)
# ax.xaxis.set_major_formatter(autoFmt)
# plt.show()

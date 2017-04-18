#################################################
##################### USAGE #####################
"""
Change variables in script then from command
line, run the command:
$ python run.py station.csv yearstart yearend
"""
#################################################
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import calendar
from scipy import signal  
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

#### Access data as numpy arrays ####
"""
dataframe is in format:
   t_datetime, pressure, t_timestamp, water_level
0           x          x           x            x
1           x          x           x            x
2           x          x           x            x
"""
t_datetime, pressure, t_timestamp, water_level = [station.as_matrix()[:,n] for n in range(1,5)]
t_datetime = np.array(list(map(lambda s: dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S'), t_datetime)))
year_index = np.array([x.year for x in t_datetime])
indices = np.where((year_index >= int(yearstart)) & (year_index <= int(yearend)))[0]

t_datetime, pressure, t_timestamp, water_level = t_datetime[indices[0]:indices[-1]], pressure[indices[0]:indices[-1]], t_timestamp[indices[0]:indices[-1]], water_level[indices[0]:indices[-1]]

water_level = water_level.astype('float')
pressure = pressure.astype('float')
water_level = water_level.astype('float')

print('Fitting tidal components, {}'.format(time.time() - start))
#### Fitting tidal component ####
water_level_average = []
windowwidth = 1  #  in array indices
for i in range(len(t_datetime)):
    lo, hi = i - windowwidth, i + windowwidth
    if lo < 0:
        lo = 0
    if hi >= len(water_level):
        hi = len(water_level) - 1
    ind_window = water_level[lo: hi]
    water_level_average.append(np.average(ind_window))
water_level_average = np.array(water_level_average)

print('Finding pressure and water level correlations, {}'.format(time.time() - start))
#### Pressure and Water Level Correlation ####
pressure_waterlevel_corrcoef = np.corrcoef(pressure,water_level)[0][1]
print("Pressure and Water Level Correlation: {}".format(pressure_waterlevel_corrcoef))

print('doing Fourier transforms, {}'.format(time.time() - start))
#### Fourier stuff ####
sp_water_level = np.fft.fft(water_level)
sp_water_level_fit = np.fft.fft(water_level_average)
freq = np.fft.fftfreq(t_timestamp.shape[0],d=1.0)

print('Finding exceedence probabilities, {}'.format(time.time() - start))
#### Exceedence Probability #####
water_level_sorted = np.sort(water_level)
water_level_rank = np.arange(len(water_level_sorted))
water_level_normalized_rank = (1.0*water_level_rank)/len(water_level_sorted)

exceedenceproball = [1 - n for n in water_level_normalized_rank]

##########################################################################################
######################################## Graphing ########################################
##########################################################################################
print('graphing, {}'.format(time.time() - start))
autoTicks = mdates.AutoDateLocator()
autoFmt = mdates.AutoDateFormatter(autoTicks)
fig = plt.figure(figsize=(20,10))

# air pressure
ax1 = fig.add_subplot(511)
ax1.plot(mdates.date2num(t_datetime),pressure,color='red')
ax1.set_ylabel('Pressure')
ax1.xaxis.set_major_locator(autoTicks)
ax1.xaxis.set_major_formatter(autoFmt)

# water level
ax2 = fig.add_subplot(512)
ax2.plot(mdates.date2num(t_datetime),water_level,color='red')
ax2.plot(mdates.date2num(t_datetime),water_level_average,color='black',linewidth=2.0) #tidal
ax2.set_ylabel('Water Level')
ax2.xaxis.set_major_locator(autoTicks)
ax2.xaxis.set_major_formatter(autoFmt)

# water level - tidal component
ax3 = fig.add_subplot(513)
ax3.plot(mdates.date2num(t_datetime),water_level - water_level_average,color='red')
ax3.set_ylabel('Residual')
ax3.xaxis.set_major_locator(autoTicks)
ax3.xaxis.set_major_formatter(autoFmt)

# signals
ax4 = fig.add_subplot(514)
ax4.plot(freq[1:int(len(freq)/2)],np.abs(sp_water_level[1:int(len(sp_water_level)/2)]),color='black')
ax4.plot(freq[1:int(len(freq)/2)],np.abs(sp_water_level_fit [1:int(len(sp_water_level_fit)/2)]),color='red')
ax4.legend(['Original Data','Fit Data'],loc=0)
ax4.set_ylabel('Signal Analysis')

# water level - tidal component
ax5 = fig.add_subplot(515)
ax5.plot(water_level_sorted,exceedenceproball)
ax5.set_ylabel('Exceedence')

plt.show()

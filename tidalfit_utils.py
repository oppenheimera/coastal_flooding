from numpy import sin, pi
from scipy.optimize import leastsq
##########################
# Tidal Fitting Utils #
##########################

#### Fitting tidal component ####
# mean_guess = 0.0
# ampM2_guess = 1.5
# ampK1_guess = 0.5
# ampK2_guess = 0.5
# phaseM2_guess = 0.05 * np.pi
# phaseK1_guess = 0.05 * np.pi
# phaseK2_guess = 0.05 * np.pi
# M2period = 12.4 * 3600  #t_timestamp in seconds
# K1period = 24.0 * 3600  #t_timestamp in seconds
# K2period = 12.0 * 3600  #t_timestamp in seconds

# data_guess = mean_guess + 
# ampM2_guess * np.sin((2 * np.pi/M2period) * t_timestamp + phaseM2_guess) +
# ampK1_guess * np.sin((2 * np.pi/K1period) * t_timestamp + phaseK1_guess) + 
# ampK2_guess * np.sin((2 * np.pi/K2period) * t_timestamp + phaseK2_guess)

# optimize_func = lambda x: x[6] 
# + x[0] * np.sin((2 * np.pi/M2period) * t_timestamp + x[1])  
# + x[2] * np.sin((2 * np.pi/K1period)*t_timestamp + x[3])  
# + x[4] * np.sin((2 * np.pi/K2period)*t_timestamp + x[5])  
# - water_level

# opt_func_args1 = [ampM2_guess, phaseM2_guess, ampK1_guess, phaseK1_guess, ampK2_guess, phaseK2_guess, mean_guess]


# ampM2_est, phaseM2_est, ampK1_est, phaseK1_est, ampK2_est, phaseK2_est, mean_est = leastsq(optimize_func, opt_func_args1)[0]
# fit_water_level = mean_est  + ampM2_est * np.sin((2*np.pi/M2period)*t_timestamp+phaseM2_est) + ampK1_est*np.sin((2*np.pi/K1period)*t_timestamp+phaseK1_est) + ampK2_est*np.sin((2*np.pi/K2period)*t_timestamp+phaseK2_est)


# first term is mean guess, constituent components after
constituents = [ 0.0, [1.5, 0.05 * pi, 12.4 * 3600], [0.5, 0.05 * pi, 24.0 * 3600], [0.5, 0.05 * pi, 12.0 * 3600] ]

# convenience function 
constituent_calc = lambda x: x[0] * sin((2 * pi / x[2]) * t_timestamp + x[1]) # array x must be in format: [amp, phase, period]


data_guess = sum([constituents[0] + sum([constituent_calc(x) for x in constituents[1:]])])


optimize_func = lambda x: x[0] + sum([x[1:][n] * sin((2 * pi / x[1:][n + 2]) * t_timestamp + x[1:][n + 1]) for n in range(len(x) - 1)[::3]]) - water_level


opt_func_args1 = [constituents[0]].extend([x for x in constituents[1:]])

ampM2_est, phaseM2_est, ampK1_est, phaseK1_est, ampK2_est, phaseK2_est, mean_est = leastsq(optimize_func, opt_func_args1)[0]
fit_water_level = mean_est  + ampM2_est * sin((2*pi/M2period)*t_timestamp+phaseM2_est) + ampK1_est*sin((2*pi/K1period)*t_timestamp+phaseK1_est) + ampK2_est*sin((2*pi/K2period)*t_timestamp+phaseK2_est)
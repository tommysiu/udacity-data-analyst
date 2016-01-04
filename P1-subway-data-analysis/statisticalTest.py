import numpy as np
from pandas import *
from ggplot import *
import scipy
import scipy.stats

def test():
    data = pandas.read_csv('turnstile_data_master_with_weather.csv')
    with_rain_mean, without_rain_mean, U, p = mann_whitney_plus_means(data)
    print 'mean(rain): %f' % with_rain_mean
    print 'mean(no rain): %f' % without_rain_mean
    print 'U-statistic: %f' % U
    print 'p-value: %.9f' % p

def mann_whitney_plus_means(turnstile_weather):
    bool_no_rain = (turnstile_weather.rain == 0)
    bool_rain = (turnstile_weather.rain == 1)
    df_norain = turnstile_weather['ENTRIESn_hourly'][bool_no_rain]
    df_rain = turnstile_weather['ENTRIESn_hourly'][bool_rain]
    with_rain_mean = np.mean(df_rain)
    without_rain_mean = np.mean(df_norain)
    U,p = scipy.stats.mannwhitneyu(df_rain, df_norain)
    
    return with_rain_mean, without_rain_mean, U, p

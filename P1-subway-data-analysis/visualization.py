from pandas import *
from pandasql import sqldf
from ggplot import *
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Function to plot first visualization
def test1():
    data = pandas.read_csv('turnstile_weather_v2.csv')
    plot_histogram(data)
    return

# Function to plot second visualization
def test2():
    data = pandas.read_csv('turnstile_weather_v2.csv')
    return plot_day_of_week_entries(data)

def plot_histogram(data):
    plt.figure()
    plt.title('Histogram of Hourly Entries')
    plt.xlabel('Hourly Entries')
    plt.ylabel('Frequency')
    b = np.arange(0, 15000, 500)
    df = data[['ENTRIESn_hourly','rain']][(data.ENTRIESn_hourly < 15000)]
    df_norain = df['ENTRIESn_hourly'][df.rain == 0]
    h_norain = df_norain.hist(bins=b, color = 'red', label = 'no rain')
    df_rain = df['ENTRIESn_hourly'][df.rain == 1]
    h_rain = df_rain.hist(bins=b, color = 'blue', label = 'rain')
    plt.legend(loc='upper right')
    return

def plot_day_of_week_entries(turnstile_weather):
    df = turnstile_weather[['day_week','ENTRIESn_hourly']].groupby(['day_week'], as_index=False).sum()
    plot = ggplot(df, aes('day_week','ENTRIESn_hourly')) + geom_point() + geom_line() + \
    ggtitle('Total Entries by Day of Week') + xlab('Day of Week') + ylab('Entries') + \
    scale_y_continuous(labels='comma') + scale_x_continuous(breaks=[0,1,2,3,4,5,6], labels=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    return plot

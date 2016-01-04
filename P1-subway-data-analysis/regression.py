import numpy as np
import pandas
import scipy.stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

def test():
    data = pandas.read_csv('turnstile_weather_v2.csv')
    p = predictions(data)
    entries = data['ENTRIESn_hourly']

    plot_residuals_hist(data,p)
    plot_residuals_probplot(data,p)

    r_squared = compute_r_squared(entries, p)
    return p,r_squared

def linear_regression(features, values):
    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]    
    return intercept, params

def predictions(dataframe):
    # Select Features (try different features!)
    features = dataframe[['rain', 'precipi', 'hour', 'weekday']]

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)

    # Values
    values = dataframe['ENTRIESn_hourly']
    
    # Get the numpy arrays
    features_array = features.values
    values_array = values.values

    # Perform linear regression
    intercept, params = linear_regression(features_array, values_array)

    predictions = intercept + np.dot(features_array, params)
    return predictions

def plot_residuals_hist(turnstile_weather, predictions):
    plt.figure()
    plt.title('Histogram of Residuals')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')

    # Plot the residual histogram
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins=100)

    return plt

def plot_residuals_probplot(turnstile_weather, predictions):
    plt.figure()

    # Plot the prob plot
    scipy.stats.probplot(x = (turnstile_weather['ENTRIESn_hourly'] - predictions), plot=plt)

    return plt

def compute_r_squared(data, predictions):
    mean = np.mean(data)
    SSres = np.sum((data-predictions)**2)
    SStot = np.sum((data-mean)**2)
    r_squared = 1 - SSres/SStot
    return r_squared

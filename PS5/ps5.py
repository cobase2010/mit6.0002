# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import numpy
import re
import math

#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers
pylab.rcParams['lines.markersize'] = 10
#set number of examples shown in legends
pylab.rcParams['legend.numpoints'] = 1

pylab.rcParams['figure.figsize'] = [10, 10]

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    #
    models = []
    for d in degs:
        model = pylab.polyfit(x, y, d)
        models.append(model)
    return models

# print(generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2, 3]))

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # 
    error = ((estimated - y)**2).sum()
    meanError = error/len(y)
    return 1 - (meanError/numpy.var(y))

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # 
    
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], x)
        error = r_squared(y, estYVals)
        pylab.figure()
        # pylab.xticks(numpy.arange(min(x), max(x)+1, 1.0))
        pylab.plot(x, y, 'bo', label = 'Measured points')
        pylab.plot(x, estYVals,'r-',
                   label = 'Model')
        # pylab.plot(x, estYVals,'r-',
        #            label = 'Fit of degree '\
        #            + str(len(models[i]) - 1)\
        #            + ', R2 = ' + str(round(error, 5)))
        pylab.legend(loc = 'best')
        if len(models[i]) == 2:
            pylab.title('Degree of Fit: ' + str(len(models[i]) - 1) + '\n' + 'R^2: ' + str(error.round(5)) + '\n' + 'Ratio of Standard Error: '
                        + str(se_over_slope(x, y, estYVals, models[i]).round(5)))
        else:
            pylab.title('Degree of Fit: ' + str(len(models[i]) - 1) + '\n' + 'R^2: ' + str(error.round(5)))
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (Celsius)')
      
        pylab.show()
    

# x = pylab.array([1961, 1962, 1963])
# y = pylab.array([-4.4, -5.5, -6.6])
# models = generate_models(x, y, [1, 2, 3])
# evaluate_models_on_training(x, y, models)
# pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    #
    temps = []
    for year in years:
        temps2 = []
        for city in multi_cities:
            temps2.append(climate.get_yearly_temp(city, year))
        temps.append(numpy.mean(temps2))
    return pylab.array(temps)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # 
    # ret = numpy.cumsum(y, dtype=float) 
    # ret[window_length:] = ret[window_length:] - ret[:-window_length]
    # return ret[window_length-1:] / window_length
    ret = []
    for i in range(len(y)):
        window = []
        if i < window_length:
            window = y[:i+1]
        else:
            window = y[i-window_length+1 : i+1]
        ret.append(numpy.mean(window))
    return pylab.array(ret) 

# y = [1, 2, 3, 4, 5, 6, 7]
# window_length = 3
# correct = pylab.array([1, 1.5, 2, 3, 4, 5, 6])
# result = moving_average(y, window_length) 
# print(result)

    

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # 
    return (((y - estimated) ** 2).sum() / len(y)) ** 0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    ret = []
    for year in years:
        # print("processing year:", year)
        days_in_year = len(climate.get_yearly_temp(multi_cities[0], year))
        # Re-wrote this using pylab array directly instead of going through each day and finding 
        # the average for each day across cities. This way is 100 times faster.
        daily_temps = pylab.zeros(days_in_year)
        for city in multi_cities:
            daily_temps += climate.get_yearly_temp(city, year)
        daily_temps = daily_temps / len(multi_cities)
        daily_mean = pylab.mean(daily_temps)
        var = 0.0
        for temp in daily_temps:
            var += (temp - daily_mean)**2
        ret.append((var / days_in_year) ** 0.5)

    return pylab.array(ret)


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # 
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], x)
        error = rmse(y, estYVals)
        pylab.figure()
        # pylab.xticks(numpy.arange(min(x), max(x)+1, 1.0))
        pylab.plot(x, y, 'bo', label = 'Measured points')
        pylab.plot(x, estYVals,'r-',
                   label = 'Model')
        pylab.legend(loc = 'best')
        
        pylab.title('Degree of Fit: ' + str(len(models[i]) - 1) + '\n' + 'rmse: ' + str(error.round(5)))
        pylab.xlabel('Year')
        pylab.ylabel('Temperature (Celsius)')
      
        pylab.show()

if __name__ == '__main__':

    pass 

    # Part A.4
    # A.4.I
    data = Climate("data.csv")
    x = pylab.array(TRAINING_INTERVAL)
    temps = []
    for year in x:
        temps.append(data.get_daily_temp('NEW YORK', 1, 10, year))
    y = pylab.array(temps)
    models = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, models)

    # A.4.II
    temps = []
    for year in x:
        temps.append(numpy.mean(data.get_yearly_temp("NEW YORK", year)))
    y = pylab.array(temps)
    # print(y)
    models = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, models)

    # Part B
    y = gen_cities_avg(data, CITIES, x)
    models = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, models)


    # Part C
    # 
    # y = moving_average(y, 5)
    # models = generate_models(x, y, [1])
    # evaluate_models_on_training(x, y, models)

    # Part D.2
    #
    # 2.1 Generate more models
    data = Climate("data.csv")
    x = pylab.array(TRAINING_INTERVAL)
    y = gen_cities_avg(data, CITIES, x)
    # y = gen_cities_avg(data, ['NEW YORK'], x)
    y = moving_average(y, 5)
    models = generate_models(x, y, [1, 2, 20])
    # evaluate_models_on_training(x, y, models)

    # 2.2 Predict the results
    x_testing = pylab.array(TESTING_INTERVAL)
    y_testing = gen_cities_avg(data, CITIES, x_testing)
    # y_testing = gen_cities_avg(data, ['NEW YORK'], x_testing)
    y_testing = moving_average(y_testing, 5)
    # evaluate_models_on_testing(x_testing, y_testing, models)


    # Part E
    # 
    std_arrays = gen_std_devs(data, CITIES, TRAINING_INTERVAL)
    std_arrays = moving_average(std_arrays, 5)
    models = generate_models(x, std_arrays, [1, 2, 20])
    evaluate_models_on_training(x, std_arrays, models)




"""
# Write up:
Part A:
1. 1/10: R^2 = 0.05348 ration of std err: 0.61368
   yearly average: R^2 = 0.18895 ratio of std err: 0.3022
   The R^2 value is much better for yearly average and the trend is more significant 
   for the yearly average case as well.
2. Daily temperature is more noisy. Noisiness is due to fluctuation of temperatures.
3. Based on yearly average data, we have a significant trend indication that yearly average
   temperature is increasing.

Part B:
1. National Avg: R^2 = 0.74616 Ration of Std Err: 0.08508
   The model with national avg represent a better fit with more significance.
2. It removes local anomalies by using national avg.
3. If the samples are random, the results should be similar.
4. 
Part C:
1. Moving avg: R^2 = 0.92498 Ratio of std err: 0.04154
2. The result fits much better with high R^2 and low RSE
3. It removes even more local and yearly fluctuations.

Part D:
2.I
deg = 1:    R^2: 0.92498
deg = 2:    R^2: 0.94482
deg = 20:   R^2: 0.97236
Degree 20 has the best fit as it was able to match the data points more fittingly:)

2.2
deg = 1:    rmse: 0.08844
deg = 2:    rmse: 0.21178
deg = 20:   rmse: 1.49123
deg = 1 has the best result as the higher degrees have problem of over-fitting.

Just for New York:
deg = 1:    rmse: 0.57821
deg = 2:    rmse: 0.92306
deg = 20:   rmse: 1.61395
It's a worse result than multi-cities due to even fewer data points.

Part E:
Standard dev over time seems going down, which means the extreme temperateure are less common.
Analysis can be improved by using a larger window length and higher degree of fit.
"""

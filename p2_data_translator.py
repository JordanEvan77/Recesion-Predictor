"""Seattle University, OMSBA 5062, DTC, Jordan Gropper

Functions:
recession_visual - plots a graphic visual showing the inverted yield curve
print_correlation - prints comparable correlations of price data

"""
import os
import csv
import matplotlib.pyplot as plt
import scipy
from scipy.stats.stats import pearsonr
from datetime import datetime
from p2_TimeSeries import TimeSeries
from p2_TimeSeries import Fred
from p2_TimeSeries import dgs3mo
from p2_TimeSeries import dgs10
from p2_TimeSeries import Bundesbank
from p2_TimeSeries import gold_spot
from p2_TimeSeries import Difference
from p2_TimeSeries import lag
from p2_TimeSeries import returns

DATA = '/Users/jorda/OneDrive/Desktop/PyCharm Community Edition 2021.2.2/5062/P2_DTC/'


def print_correlations():
    """A function set up for the ease of running the correlations function in the TimeSeries file
    with both the difference of the treasury assets paired with the gold prices, but also the
    gold prices along with a lagged selling profit."""
    short = dgs3mo()
    long = dgs10()
    gold = gold_spot()
    dates = short.get_dates()
    dates = long.get_dates(dates)  # dates is now the intersection
    diff = long - short
    gold_correlation, pval = gold.correlation(diff)
    print('Correlation between dgs10-dgs3mo and gold_spot: {:.2%}'.format(gold_correlation))
    # help with print formatting from Brooke
    buy_lag = 3  # will hold usually but should not be hard coded!
    hold_time = 20  # these are just temporary
    investment = returns(gold, hold_time)  # looks to be working
    signal = diff  # working
    compare_to = lag(signal, buy_lag + hold_time)  # looks to be working
    signal_to_result_correlation, pval = investment.correlation(compare_to)
    print("Correlation between dgs10-dgs3mo and gold returns (" + str(buy_lag) +
          " days wait, " + str(hold_time) + " day hold): {:.2%}".format(
        signal_to_result_correlation))  # help with print formatting from Brooke


def recession_visual():
    """Plot a graphic visual showing the inverted yield curve for the treasurey assets and the
    compared gold price curve"""
    short = dgs3mo()
    long = dgs10()
    gold = gold_spot()
    dates = short.get_dates()
    dates = long.get_dates(dates)  # dates is now the intersection
    gold_date = gold.get_dates(dates)
    gold_val = gold.get_values(dates)
    diff = long - short
    y_diff = diff.get_values(dates)
    x_dates = diff.get_dates(candidates=dates)

    fig = plt.figure(1)
    ax = fig.add_subplot(111)  # working
    left = ax.plot(gold_date, gold_val, color='orange')
    ax.set_ylabel('USD per ounce')
    ax.set_xlabel('date')
    axr = ax.twinx()  # left and right y axes share the x axis
    right = axr.plot(x_dates, y_diff)
    axr.set_ylabel('percent per anum')  # want to share the axis
    axr.axhline(y=0, color='r')
    fig.autofmt_xdate()  # nice dates on x axis
    ax.legend(left + right, ['gold_spot', 'dgs10-dgs3mo'],
              loc='upper center')
    ax.set_title('Gold vs. Yield Curve Inversion')
    plt.show()


if __name__ == '__main__':
    print_correlations()
    recession_visual()
# seems to be working!

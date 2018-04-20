from datetime import date as dt
from calendar import monthrange
from pandas.tseries.offsets import BDay

def is_bday(date):  # move to date utils
    return (date + BDay(0)).date() == date

def month_ends_range(start, end):  # move to date lib
    months_ends = [
        dt(y, m, monthrange(y, m)[1]) 
        for y in range(start.year, end.year + 1) for m in range(1, 13)
    ]
    return [d for d in months_ends if d >= start and d <= end]

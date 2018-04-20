from .stock import Stock
from .portfolio import Portfolio
from datetime import date as dt

ITOT = Stock('ITOT')
# IEFA = Stock('IEFA')
ACWI = Stock('ACWI')
# AGG = Stock('AGG')

port = Portfolio()
port.build_VA_portfolio(
    [ITOT, ACWI], 
    [0.5, 0.5],
    2000,
    dt(2016, 12, 31),
    dt(2017, 9, 30)
)

print("\n\nTRANSACTIONS:")
print(port.transactions)
print("\n\nPORT:")
print(port)
print(port.weights())

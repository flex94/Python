"""Models a portfolio of stocks."""
from ..utils.dates import month_ends_range
from datetime import date as dt  # , timedelta
import pandas as pd
from pandas.tseries.offsets import BDay
# import pdb

class Position:
    def __init__(self, stock, qty):
        self.stock = stock
        self.qty = qty

    def value(self, date):
        return self.qty * self.stock.close(date)

    def _transaction(self, qty):
        return Position(self.stock, self.qty + qty)

    def __repr__(self):
        return "{0} * {1!s}".format(self.qty, self.stock)

class Holdings:
    def __init__(self, pos=[]):
        self.pos = [Position(stock, qty) for stock, qty in pos]

    def _reduce_pos(self):
        new_pos = []
        for stk in self.stocks():
            new_pos.append(
                Position(
                    stk,
                    sum([p.qty for p in self.pos if p.stock == stk])
                )
            )
        self.pos = new_pos
        return self

    def transaction(self, trans):
        hld = Holdings()
        hld.pos.extend(self.pos)
        for stk, qty in trans:
            hld.pos.append(Position(stk, qty))
        return hld._reduce_pos()

    def agg_value(self, date=(dt.today() - BDay(1)).date()):
        return sum([p.value(date) for p in self.pos])

    def value(self, stock, date=(dt.today() - BDay(1)).date()):
        return sum([p.value(date) for p in self.pos if p.stock == stock])

    def stocks(self):
        return set([p.stock for p in self.pos])

    def weights(self, date):
        agg_val = self.agg_value(date)
        return [
            [stk, self.value(stk, date) / agg_val] 
            for stk in self.stocks()
        ] 

    def __add__(self, h2):
        hld = Holdings()
        hld.pos = self.pos + h2.pos
        return hld._reduce_pos()

    def __repr__(self):
        return " + ".join(["{!s}".format(p) for p in self.pos])

class Portfolio:
    def __init__(self):
        self.holdings = pd.Series()
        self.transactions = pd.Series()

    def add_holdings(self, hld, date):
        self.holdings.set_value(date, hld)
        return self

    def make_transaction(self, trans, start, end):  
        hs = self.holdings[start]
        if end in self.holdings.keys():
            he = self.holdings[end]  
        else:
            he = Holdings()
        self.holdings[end] = he + hs.transaction(trans)  
        self.transactions.set_value(end, trans)
        return self

    def agg_value(self, date=None):
        if not date:
            date = max(self.holdings.keys())
        return self.holdings[date].agg_value(date)

    def value(self, stock, date=None):
        if not date:
            date = max(self.holdings.keys())
        return self.holdings[date].value(stock, date)

    def stocks(self, date=None):
        if not date:
            date = max(self.holdings.keys())
        return self.holdings[date].stocks()

    #def get_holdings(self, date=None):
        #if not date:
            #date = max(self.holdings.keys())
        #return self.holdings[date]

    def weights(self, date=None):
        if not date:
            date = max(self.holdings.keys())
        return self.holdings[date].weights(date)

    def __repr__(self):
        return str(self.holdings)

    def build_VA_portfolio(self, stocks, wgts, incr, start, end):
        dates = month_ends_range(start, end)
        tgt_val = incr

        # Initialize holdings
        date = dates[0]
        hld = Holdings([
            [
                stk,
                self._calc_qty(stk, date, wgt * incr)
            ]
            for stk, wgt in zip(stocks, wgts)
        ])
        self.add_holdings(hld, date)

        # Iterate on dates
        for t in range(1, len(dates)):
            wgts = self.weights(dates[t - 1])
            transactions = []
            tgt_val += incr
            for stk, wgt in wgts:
                incr_val = tgt_val * wgt - self.value(stk, dates[t - 1])
                incr_qty = self._calc_qty(stk, dates[t], incr_val)
                transactions.append([stk, incr_qty])  # todo: add as attr
            self.make_transaction(transactions, dates[t - 1], dates[t])

        return self

    @staticmethod
    def _calc_qty(stock, date, tgt_val):
        return round(tgt_val / stock.close(date))

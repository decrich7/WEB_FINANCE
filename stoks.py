import matplotlib.pyplot as plt
import yfinance as yf
from pypfopt.cla import CLA
import pypfopt.plotting as pplt
from matplotlib.ticker import FuncFormatter
from pypfopt import expected_returns, risk_models, EfficientFrontier, get_latest_prices, \
    DiscreteAllocation


class Stock():
    def __init__(self, tickers, money, shorts=True):
        self.shorts = shorts
        self.money = money
        if self.shorts:
            self.shorts = 0
        else:
            self.shorts = -1
        # tickers = ['F', 'AAPL', 'GE', 'BAC', 'PLUG', 'AMD']
        self.df_stocks = yf.download(tickers, period='1Y')['Adj Close']
        self.mu = expected_returns.mean_historical_return(self.df_stocks)
        self.Sigma = risk_models.sample_cov(self.df_stocks)
        self.ef = EfficientFrontier(self.mu, self.Sigma, weight_bounds=(self.shorts, 1))
        self.sharpe_pfolio = self.ef.max_sharpe()
        self.sharpe_pwt = self.ef.clean_weights()
        self.ef1 = EfficientFrontier(self.mu, self.Sigma, weight_bounds=(self.shorts, 1))
        self.minvol = self.ef1.min_volatility()
        self.minvol_pwt = self.ef1.clean_weights()
        self.latest_prices = get_latest_prices(self.df_stocks)

    def profit(self):
        self.performance = self.ef.portfolio_performance()
        return f'{round(self.performance[0] * 100, 2)}%'

    def volatility(self):
        allocation_minv, rem_minv = DiscreteAllocation(self.minvol_pwt, self.latest_prices,
                                                       total_portfolio_value=self.money).lp_portfolio()
        self.dict_minv = {}
        for i, j in allocation_minv.items():
            self.dict_minv[i] = int(j)
        return self.dict_minv, "{:.2f}".format(rem_minv)

    def plot_equal_volatility(self, id_user):
        fig, ax = plt.subplots()
        ax.pie(self.dict_minv.values(), labels=self.dict_minv.keys(), autopct='%1.1f%%', rotatelabels=True)
        ax.axis("equal")
        plt.savefig(f'static/plot/plot_equal_volatility_{id_user}.png')
        return f'static/plot/plot_equal_volatility_{id_user}.png'

    def sharp(self):
        allocation_shp, rem_shp = DiscreteAllocation(self.sharpe_pwt, self.latest_prices,
                                                     total_portfolio_value=self.money).lp_portfolio()
        self.dict_shp = {}
        for i, j in allocation_shp.items():
            self.dict_shp[i] = int(j)
        return self.dict_shp, "{:.2f}".format(rem_shp)

    def plot_equal_sharp(self, id_user):
        fig, ax = plt.subplots()
        ax.pie(self.dict_shp.values(), labels=self.dict_shp.keys(), autopct='%1.1f%%', rotatelabels=True)
        ax.axis("equal")
        plt.savefig(f'static/plot/plot_equal_sharp_{id_user}.png')
        return f'static/plot/plot_equal_sharp_{id_user}.png'

    def plot(self, id_user):
        cl_obj = CLA(self.mu, self.Sigma)
        ax = pplt.plot_efficient_frontier(cl_obj, showfig=False)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        plt.savefig(f'static/plot/plot_{id_user}.png')
        return f'static/plot/plot_{id_user}.png'

# a = Stock(1000)
# print(a.volatility())
# print(a.profit())
# print(a.sharp())
# print(a.plot_equal_volatility())


# import requests
# print(requests.get(f'http://127.0.0.1:5000/api/v2/briefcase/2'))
# print(requests.post('http://127.0.0.1:5000/api/v2/briefcase/', json={
#             'date': 423,
#             'length_invest_horizon': 1,
#             'budget': 10000,
#             'tg_id': 23424234,
#             'shorts': True
#         }).content)

# print(requests.get('http://127.0.0.1:5000/api/v2/briefcase/').content)

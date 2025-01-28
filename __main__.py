import pandas as pd
from core.backtester import Backtester
from strategies.strategy import Strategy    

data = pd.read_csv("hindsight/FINNIFTY-INDEX.csv")
data.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
data.set_index("datetime")  


class TradingStrategy(Strategy):
    def precompute(self):
        # price = [row['close'] for row in self.__data]
        # self.ma1 = self.get_indicator_output(Indicators.SMA, price, 10)
        pass
    def decide(self, row, row_idx):
        if row_idx >= 3:
            third = self.data.iloc[row_idx - 3]
            second = self.data.iloc[row_idx - 2]
            first = self.data.iloc[row_idx - 1]
        
            if third['close'] > third['open'] and second['close'] > second['open'] and first['close'] > first['open']:
                return 1
            elif  third['close'] < third['open'] and second['close'] < second['open'] and first['close'] < first['open']:
                return -1
            return 0
        else:
            return 0

# Initialize and run backtester
backtester = Backtester(data, TradingStrategy, funds=100000, transaction_cost=0.1)
backtester.start()

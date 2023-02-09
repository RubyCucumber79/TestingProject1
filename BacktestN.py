from oneHR import *
from backtesting import Strategy
from backtesting import Backtest

df=dataF()
#df.reset_index(level=0, inplace=True)
df=df.dropna()
df.reset_index(drop=True, inplace=True)
df.isna().sum()
#print(df.signal)

def SIGNAL1():
    return df.signal

#print(type(SIGNAL))
class MyCandlesStrat(Strategy):  
    def init(self):
        super().init()
        self.signal2 = self.I(SIGNAL1)

    def next(self):
        super().next() 
        if self.signal2==2:
            sl1 = self.data.Close[-1] - (self.data.Close[-1]*0.06)
            tp1 = self.data.Close[-1] + (self.data.Close[-1]*0.05)
            self.buy(sl=sl1, tp=tp1)
        elif self.signal2==1:
            sl1 = self.data.Close[-1] + (self.data.Close[-1]*0.05)
            tp1 = self.data.Close[-1] - (self.data.Close[-1]*0.06)
            self.sell(sl=sl1, tp=tp1)

bt = Backtest(df, MyCandlesStrat, cash=10_000, commission=.002)
stat = bt.run()
print(stat)          

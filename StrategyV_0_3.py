from oneHR import *
from backtesting import Strategy
from backtesting import Backtest


df = dataF()
length = len(df)
high = list(df['High'])
low = list(df['Low'])
close = list(df['Close'])
open = list(df['Open'])
signal = [0] * length

for row in range(1,length):
    if ((high[row-1]<high[row]) and (open[row]<close[row])):
        signal[row]=2
    elif((high[row-1]>high[row]) and (open[row]>close[row])):
        signal[row]=1
    elif((high[row-1]<high[row]) and (open[row]>close[row])):
        signal[row]=1
    elif((low[row-1]<low[row]) and (open[row]<close[row])):
        signal[row]=2
    elif((low[row-1]>low[row]) and (open[row]>close[row])):
        signal[row]=1
    elif((low[row-1]<low[row]) and (open[row]>close[row])):
        signal[row]=1
    else:
        signal[row]=0

df['signal']=signal
print(df[df['signal']!=0].count())

df=df.dropna()
df.reset_index(drop=True, inplace=True)
df.isna().sum()

def SIGNAL1():
    return df.signal

class MyCandlesStrat(Strategy):  
    def init(self):
        super().init()
        self.signal2 = self.I(SIGNAL1)

    def next(self):
        super().next() 
        if self.signal2==2:
            sl1 = self.data.Close[-1] - (self.data.Close[-1]*0.05)
            tp1 = self.data.Close[-1] + (self.data.Close[-1]*0.01)
            self.buy(sl=sl1, tp=tp1)
        elif self.signal2==1:
            sl1 = self.data.Close[-1] + (self.data.Close[-1]*0.05)
            tp1 = self.data.Close[-1] - (self.data.Close[-1]*0.01)
            self.sell(sl=sl1, tp=tp1)

bt = Backtest(df, MyCandlesStrat, cash=10_000, commission=.002)
stat = bt.run()
print(stat)    
         
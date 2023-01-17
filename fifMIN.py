import pandas as pd
from plottingCandlesticks import *
from Main import *

df = pd.read_csv("NIFTY_2014.csv")

df["DateTime"] = df["Date"].astype(str)+ " " + df["Time"].astype(str)
df['DateTime'] = pd.to_datetime(df['DateTime'])
df.set_index('DateTime',inplace=True)


df_15min = df.resample('15T', closed='left', label='left').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'})
dfN=df_15min.head(15)
dfN['Date']=dfN.index
#print(dfN)
#plot_candlesticks(df_15min.head(15))
findCandlestick(dfN)
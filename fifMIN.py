import pandas as pd
from plottingCandlesticks import *
from Npatterns import *
from SR import *


df = pd.read_csv(r"D:\WORK\TestingProject1\NIFTY_2014.csv")

df["DateTime"] = df["Date"].astype(str)+ " " + df["Time"].astype(str)
df['DateTime'] = pd.to_datetime(df['DateTime'])
df.set_index('DateTime',inplace=True)


df_15min = df.resample('15T', closed='left', label='left').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'})
#dfN=df_15min
#dfN=dfN.dropna(subset=['Open'])

#df_15min.reset_index(level=0, inplace=True)
#df_15min=df_15min.dropna().reset_index(drop=True)
#dfN=dfN.dropna().reset_index(drop=True)
#df_15min=dfN


#df_15min['signal1'] = Revsignal1(df_15min)
#df_15min['Trend1'] = mytarget(df_15min,3)
#print(df_15min)
#accuracy(df_15min)
#bands(df_15min)
#fP(df_15min)
#print(df_15min[df_15min['signal1']==1].count()) #bearish

length = len(df_15min)
high = list(df_15min['High'])
low = list(df_15min['Low'])
close = list(df_15min['Close'])
open = list(df_15min['Open'])
bodydiff = [0] * length

highdiff = [0] * length
lowdiff = [0] * length
ratio1 = [0] * length
ratio2 = [0] * length

def isEngulfing(l):
    row=l
    bodydiff[row] = abs(open[row]-close[row])
    if bodydiff[row]<0.000001:
        bodydiff[row]=0.000001      

    bodydiffmin = 0.002
    if (bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
        open[row-1]<close[row-1] and
        open[row]>close[row] and 
        (open[row]-close[row-1])>=-0e-5 and close[row]<open[row-1]):
        return 1

    elif(bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
        open[row-1]>close[row-1] and
        open[row]<close[row] and 
        (open[row]-close[row-1])<=+0e-5 and close[row]>open[row-1]):
        return 2
    else:
        return 0
       
def isStar(l):
    bodydiffmin = 0.0020
    row=l
    highdiff[row] = high[row]-max(open[row],close[row])
    lowdiff[row] = min(open[row],close[row])-low[row]
    bodydiff[row] = abs(open[row]-close[row])
    if bodydiff[row]<0.000001:
        bodydiff[row]=0.000001
    ratio1[row] = highdiff[row]/bodydiff[row]
    ratio2[row] = lowdiff[row]/bodydiff[row]

    if (ratio1[row]>1 and lowdiff[row]<0.2*highdiff[row] and bodydiff[row]>bodydiffmin):
        return 1
    elif (ratio2[row]>1 and highdiff[row]<0.2*lowdiff[row] and bodydiff[row]>bodydiffmin):
        return 2
    else:
        return 0
    
def closeResistance(l,levels,lim):
    if len(levels)==0:
        return 0
    c1 = abs(df_15min.High[l]-min(levels, key=lambda x:abs(x-df_15min.High[l])))<=lim
    c2 = abs(max(df_15min.Open[l],df_15min.Close[l])-min(levels, key=lambda x:abs(x-df_15min.High[l])))<=lim
    c3 = min(df_15min.Open[l],df_15min.Close[l])<min(levels, key=lambda x:abs(x-df_15min.High[l]))
    c4 = df_15min.Low[l]<min(levels, key=lambda x:abs(x-df_15min.High[l]))
    if( (c1 or c2) and c3 and c4 ):
        return 1
    else:
        return 0
    
def closeSupport(l,levels,lim):
    if len(levels)==0:
        return 0
    c1 = abs(df_15min.Low[l]-min(levels, key=lambda x:abs(x-df_15min.Low[l])))<=lim
    c2 = abs(min(df_15min.Open[l],df_15min.Close[l])-min(levels, key=lambda x:abs(x-df_15min.Low[l])))<=lim
    c3 = max(df_15min.Open[l],df_15min.Close[l])>min(levels, key=lambda x:abs(x-df_15min.Low[l]))
    c4 = df_15min.High[l]>min(levels, key=lambda x:abs(x-df_15min.Low[l]))
    if( (c1 or c2) and c3 and c4 ):
        return 1
    else:
        return 0

n1=6
n2=6
backCandles=15
signal = [0] * length

for row in range(backCandles, len(df_15min)-n2):
    ss = []
    rr = []
    for subrow in range(row-backCandles+n1, row+1):
        if support(df_15min, subrow, n1, n2):
            ss.append(df_15min.Low[subrow])
        if resistance(df_15min, subrow, n1, n2):
            rr.append(df_15min.High[subrow])
    
    if ((isEngulfing(row)==1 or isStar(row)==1) and closeResistance(row, rr, 150e-5) ):
        signal[row] = 1
    elif((isEngulfing(row)==2 or isStar(row)==2) and closeSupport(row, ss, 150e-5)):
        signal[row] = 2
    else:
        signal[row] = 0

df_15min['signal']=signal
def dataF():
    return df_15min
          

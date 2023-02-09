
import numpy as np
def Revsignal1(df1):
    length = len(df1)
    high = list(df1['High'])
    low = list(df1['Low'])
    close = list(df1['Close'])
    open = list(df1['Open'])
    signal = [0] * length
    bodydiff = [0] * length

    for row in range(1, length):
        bodydiff[row] = abs(open[row]-close[row])
        bodydiffmin = 0.003
        if (bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
            open[row-1]<close[row-1] and
            open[row]>close[row] and 
            #open[row]>=close[row-1] and close[row]<open[row-1]):
            (open[row]-close[row-1])>=+0e-5 and close[row]<open[row-1]):
            signal[row] = 1
        elif (bodydiff[row]>bodydiffmin and bodydiff[row-1]>bodydiffmin and
            open[row-1]>close[row-1] and
            open[row]<close[row] and 
            #open[row]<=close[row-1] and close[row]>open[row-1]):
            (open[row]-close[row-1])<=-0e-5 and close[row]>open[row-1]):
            signal[row] = 2
        else:
            signal[row] = 0
        #signal[row]=random.choice([0, 1, 2])
        #signal[row]=1
    return signal


#Target
def mytarget(df1, barsfront):
    length = len(df1)
    high = list(df1['High'])
    low = list(df1['Low'])
    close = list(df1['Close'])
    open = list(df1['Open'])
    trendcat = [None] * length
    
    piplim = 300e-5
    for line in range (0, length-1-barsfront):
        for i in range(1,barsfront+1):
            if ((high[line+i]-max(close[line],open[line]))>piplim) and ((min(close[line],open[line])-low[line+i])>piplim):
                trendcat[line] = 3 # no trend
            elif (min(close[line],open[line])-low[line+i])>piplim:
                trendcat[line] = 1 #-1 downtrend
                break
            elif (high[line+i]-max(close[line],open[line]))>piplim:
                trendcat[line] = 2 # uptrend
                break
            else:
                trendcat[line] = 0 # no clear trend  
    return trendcat

def accuracy(df):
    conditions = [(df['Trend1'] == 1) & (df['signal1'] == 1),(df['Trend1'] == 2) & (df['signal1'] == 2)]
    values = [1, 2]
    df['result'] = np.select(conditions, values)

    trendId=2
    print("percent by which it was uptrend after bullish engulfing pattern: " , df[df['result']==trendId].result.count()/df[df['signal1']==trendId].signal1.count())
    trendId=1
    print("percent by which it was downtrend after bearish engulfing pattern: ", df[df['result']==trendId].result.count()/df[df['signal1']==trendId].signal1.count())
    

def fP(df):
    trendId=2
    print(df[ (df['Trend1']!=trendId) & (df['signal1']==trendId) ]) # false positives
    trendId=1
    print(df[ (df['Trend1']!=trendId) & (df['signal1']==trendId) ]) # false positives
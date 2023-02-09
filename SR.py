import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
def support(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.Low[i]>df1.Low[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.Low[i]<df1.Low[i-1]):
            return 0
    return 1



def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
    for i in range(l-n1+1, l+1):
        if(df1.High[i]<df1.High[i-1]):
            return 0
    for i in range(l+1,l+n2+1):
        if(df1.High[i]>df1.High[i-1]):
            return 0
    return 1

def bands(df):
    sr = []
    n1=3
    n2=2
    for row in range(3, 205): #len(df)-n2
        if support(df, row, n1, n2):
            sr.append((row,df.Low[row],1))
        if resistance(df, row, n1, n2):
            sr.append((row,df.High[row],2))
    
    plotlist1 = [x[1] for x in sr if x[2]==1]
    plotlist2 = [x[1] for x in sr if x[2]==2]
    plotlist1.sort()
    plotlist2.sort()

    for i in range(1,len(plotlist1)):
        if(i>=len(plotlist1)):
            break
        if abs(plotlist1[i]-plotlist1[i-1])<=0.005:
            plotlist1.pop(i)

    for i in range(1,len(plotlist2)):
        if(i>=len(plotlist2)):
            break
        if abs(plotlist2[i]-plotlist2[i-1])<=0.005:
            plotlist2.pop(i)
        plotlist2

    s = 0
    e = 121
    dfpl = df[s:e]


    fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                    open=dfpl['Open'],
                    high=dfpl['High'],
                    low=dfpl['Low'],
                    close=dfpl['Close'])])

    c=0
    while (1):
        if(c>len(plotlist1)-1 ):#or sr[c][0]>e
            break
        fig.add_shape(type='line', x0=s, y0=plotlist1[c],
                      x1=e,
                      y1=plotlist1[c],
                      line=dict(color="Orange",width=3)
                    ) 
        c+=1

    c=0
    while (1):
        if(c>len(plotlist2)-1 ):#or sr[c][0]>e
            break
        fig.add_shape(type='line', x0=s, y0=plotlist2[c],
                      x1=e,
                      y1=plotlist2[c],
                      line=dict(color="RoyalBlue",width=1)
                    )
        c+=1    

    fig.show()
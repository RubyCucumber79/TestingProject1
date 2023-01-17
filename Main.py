from candlestick import candlestick
import candlestick
import pandas as pd
import requests

# Workf from here : Create block function to read the csv file into the date time format to detect pattern
def findCandlestick(df):
    candles_df = df
    candles_df=candles_df.loc['DateTime']  
    #pd.to_datetime(candles_df['DateTime'], unit='s')

    print(candles_df.head(10))

    target = 'bearish_harami'
    #candles_df = candlestick.inverted_hammer(candles_df, target=target)
    #candles_df = candlestick.doji_star(candles_df, target=target)
    #candles_df = candlestick.bearish_harami(candles_df, target=target)
    candles_df = candlestick.bullish_harami(candles_df, target=target)
    # candles_df = candlestick.dark_cloud_cover(candles_df)
    # candles_df = candlestick.doji(candles_df)
    # candles_df = candlestick.dragonfly_doji(candles_df)
    # candles_df = candlestick.hanging_man(candles_df)
    # candles_df = candlestick.gravestone_doji(candles_df)
    # candles_df = candlestick.bearish_engulfing(candles_df)
    # candles_df = candlestick.bullish_engulfing(candles_df)
    # candles_df = candlestick.hammer(candles_df)
    # candles_df = candlestick.morning_star(candles_df)
    # candles_df = candlestick.morning_star_doji(candles_df)
    # candles_df = candlestick.piercing_pattern(candles_df)
    # candles_df = candlestick.rain_drop(candles_df)
    # candles_df = candlestick.rain_drop_doji(candles_df)
    # candles_df = candlestick.star(candles_df)
    # candles_df = candlestick.shooting_star(candles_df)

    print(candles_df[candles_df[target] == True][['T', target]])
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 21:14:14 2017

@author: Peng
"""
#%matplotlib inline
import matplotlib.dates as dates
import matplotlib.finance as f  
import matplotlib.pyplot as plt
import datetime
import pandas as pd

date1 = datetime.date( 2017, 1, 1 )
date2 = datetime.date( 2017, 3, 20 )
sp = f.quotes_historical_yahoo_ohlc('000049.sz', date1, date2, adjusted=True)
df = pd.DataFrame(sp, columns=['date','open','high','low','close','volume'])
df['date'] = dates.num2date(df['date'])
df = df[df['volume'] != 0]
#print df

## draw volume chart
#temp_df = df[df['date'] >= datetime.date( 2016, 2, 1 )]
#fig, ax = plt.subplots()
#ax = temp_df['volume'].plot(kind='Bar', color=['r' if x[5] > x[2] else 'g' for x in temp_df.itertuples()])
#ax.set_xticklabels([x.strftime('%Y-%m-%d') for x in temp_df['date']])
##fig.show()

# calculate volume mean 
temp_df = df
params = [5, 10, 20]
for p in params:
    temp_df['vol'+str(p)] = pd.rolling_mean(df['volume'], window=p)
temp_df = temp_df[temp_df['date'] >= datetime.date( 2016, 2, 1 )]
print temp_df

#fig.show()
## draw volume mean chart
fig, ax = plt.subplots()
param_colors = [(1,0.7,0.2), (0,0.7,0.9), (0.9,0.5,0.9)]
for (i,p) in enumerate(params):
    temp_df[['vol'+str(p)]].plot(kind='line', ax=ax, color=param_colors[i], use_index=False)
temp_df[['volume']].plot(kind='bar', ax=ax, color=['r' if x[5] > x[2] else 'g' for x in temp_df.itertuples()])
ax.set_xticklabels([x.strftime('%Y-%m-%d') for x in temp_df['date']])
plt.show()

# draw MA line
temp_df = df
params = [5, 10, 20]
for p in params:
    temp_df['ma'+str(p)] = pd.rolling_mean(df['close'], window=p)
temp_df = temp_df[temp_df['date'] >= datetime.date( 2016, 2, 1 )]
fig, ax = plt.subplots(1)
param_colors = [(1,0.7,0.2), (0,0.7,0.9), (0.9,0.5,0.9)]
for (i,p) in enumerate(params):
    temp_df[['ma'+str(p)]].plot(kind='line', ax=ax, color=param_colors[i], use_index=False)
ax.set_xticklabels([x.strftime('%d') for x in temp_df['date']])
fig.show()

# draw EMA line
params = [5, 10, 20]
for p in params:
    temp_df['ema'+str(p)] = pd.ewma(temp_df['close'], span=p)
temp_df = temp_df[temp_df['date'] >= datetime.date( 2016, 2, 1 )]
fig, ax = plt.subplots()
param_colors = [(1,0.7,0.2), (0,0.7,0.9), (0.9,0.5,0.9)]
for (i,p) in enumerate(params):
    temp_df[['ema'+str(p)]].plot(kind='line', ax=ax, color=param_colors[i], use_index=False)
ax.set_xticklabels([x.strftime('%d') for x in temp_df['date']])
fig.show()

#calculate MACD
date1 = datetime.date( 2015, 6, 1 )
date2 = datetime.date( 2016, 2, 20 )
sp = f.quotes_historical_yahoo_ohlc('601233.ss', date1, date2, adjusted=True)
temp_df = pd.DataFrame(sp, columns=['date','open','high','low','close','volume'])
temp_df['date'] = dates.num2date(temp_df['date'])
temp_df = temp_df[temp_df['volume'] != 0]

params = [12, 26]
for p in params:
    temp_df['ema'+str(p)] = pd.ewma(temp_df['close'], span=p)
temp_df['DIF'] = temp_df['ema12'] - temp_df['ema26']
temp_df['DEM'] = pd.ewma(temp_df['DIF'], span=9)
temp_df['MACD'] = (temp_df['DIF'] - temp_df['DEM']) * 2
temp_df = temp_df[temp_df['date'] >= datetime.date( 2015, 12, 1 )]

#draw macd
fig, ax = plt.subplots()
param_colors = [(1,0.7,0.2), (0,0.7,0.9), (0.9,0.5,0.9)]
temp_df[['DIF','DEM']].plot(kind='line', ax=ax, color=param_colors, use_index=False)
temp_df[['MACD']].plot(kind='bar', ax=ax, color=['r' if x[-1] > 0 else 'g' for x in temp_df.itertuples()])
ax.set_xticklabels([x.strftime('%d') for x in temp_df['date']])
fig.show()

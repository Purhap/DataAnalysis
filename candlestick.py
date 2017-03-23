#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 19:39:30 2017

@author: Peng
"""

#draw K line
import sys
import datetime
import numpy as np
import math
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.finance as f
import bisect



stockcode = '000049.sz'
date1 = datetime.date( 2016, 1, 1 )
#date2 = datetime.date( 2017, 3, 20 )
date2 = datetime.date.today()
stockcode = '000049.sz'

def millions(x, pos):
    return '1.1fM' % (x*1e-6)

def thousands(x, pos):
    return '1.1fK' % (x*1e-3)

def format_coord1(x,y):
    return 'x=%s, y=%1.1f' %(r.date[x+0.5],y)

def format_coord2(x, y):
    return 'x=%s, y=%1.1fM' % (r.date[x+0.5], y*1e-6)


def getListOfDates(startdate, enddate):
    dates = [datetime.date(m/12, m%12+1, 1) for m in range(startdate.year*12+ startdate.month -1, enddate.year*12+enddate.month)]
    return np.array(dates)

def getDateIndex(dates, tickdates):
    index = [bisect.bisect_left(dates, tickdate) for tickdate in tickdates]
    return np.array(index)

def getMonthNames(dates, index):
    names = [dates[i].strftime("%b'%y") for i in index]
    return np.array(names)


def MA(x,n, type='simple'):
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1.,0.,n))
    weights /= weights.sum()
    
    a = np.convolve(x,weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def DonchianHi(x, n):
    x = np.asarray(x)
    a = np.ones(len(x))
    i = len(x) - 1
    while i > 0:
        s = i - n
        if s < 0: s = 0
        a[i]=x[s:i].max()
        i = i - 1
    a[i]=x[i]
    return a

def DonchianLo(x, n):
    x = np.asarray(x)
    a = np.ones(len(x))
    i = len(x) - 1
    while i > 0:
        s = i - n
        if s < 0: s = 0
        a[i]=x[s:i].min()
        i = i - 1
    a[i]=x[i]
    return a

def MACD(x, nslow=26, nfast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = moving_average(x, nslow, type='exponential')
    emafast = moving_average(x, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow         
    
#r = f.quotes_historical_yahoo_ohlc(stockcode, date1, date2, adjusted=True)
fh = f.fetch_historical_yahoo(stockcode, date1, date2)
r = mlab.csv2rec(fh); fh.close()
r.sort()
if len(r.date)==0:
    raise SystemExit

tickdates = getListOfDates(date1, date2)
tickindex = getDateIndex(r.date, tickdates)
ticknames = getMonthNames(r.date, tickindex)

formatter = mpl.dates.IndexDateFormatter(mpl.dates.date2num(r.date), '%m/%d/%y')

millionformatter = mpl.ticker.FuncFormatter(millions)
thousandformatter = mpl.ticker.FuncFormatter(thousands)

fig = plt.figure()
fig.subplots_adjust(bottom=0.1)
fig.subplots_adjust(hspace=0)

gs = mpl.gridspec.GridSpec(2,1, height_ratios =[4,1])
ax0 = plt.subplot(gs[0])

candles = f.candlestick2_ohlc(ax0, r.open, r.high, r.low, r.close, colorup='r', colordown='g', width=1)

ma05 = MA(r.close, 5, type='simple')
ma10 = MA(r.close, 10, type='simple')
ma20 = MA(r.close, 20, type='simple')
ma30 = MA(r.close, 30, type='simple')
ma60 = MA(r.close, 60, type='simple')
ma120 = MA(r.close, 120, type='simple')

Don20Hi = DonchianHi(r.high, 20)
Don20Lo = DonchianLo(r.low, 20)

ax0.plot(ma05, lw=2, label='MA (5)')
ax0.plot(ma10, lw=2, label='MA (10)')
ax0.plot(ma20, lw=2, label='MA (20)')
ax0.plot(ma30, lw=2, label='MA (30)')
ax0.plot(ma60, lw=2, label='MA (60)')
ax0.plot(ma120, lw=2, label='MA (120)')
#ax0.plot(Don20Hi, color='blue', lw=2, ls='--', label='DonHi (20)')
#ax0.plot(Don20Lo, color='blue', lw=2, ls='--', label='DonLo (20)')
    
ax0.set_xticks(tickindex)
ax0.set_xticklabels(ticknames,)
ax0.format_coord = format_coord1
ax0.legend(loc='best', shadow=True, fancybox=True)
ax0.set_ylabel('Price(RMB)', fontsize=16)
ax0.set_title(stockcode, fontsize=24, fontweight='bold')
ax0.grid(True)

ax1 = plt.subplot(gs[1], sharex=ax0)

vc = f.volume_overlay(ax1, r.open, r.close, r.volume, colorup='r', colordown='g', width=1)
#ax1.set_xtick(tickindex)
ax1.set_xticklabels(ticknames)
ax1.format_coord = format_coord2

ax1.tick_params(axis='x', direction='out', length=5)
ax1.yaxis.set_major_formatter(millionformatter)
ax1.yaxis.tick_right()
ax1.yaxis.set_label_position("right")
ax1.set_ylabel('Volume', fontsize=16)
ax1.grid(True)

#plt.setp(ax0.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
fig = plt.gcf()
#fig.set_size_inches(18.5, 10.5)
fig.set_size_inches(37, 21)
fig.savefig('test2png.png', dpi=300)
plt.show()

#plt.savefig('./test1.png')
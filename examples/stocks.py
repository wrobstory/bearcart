#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
An example for Bearcart
'''
import datetime

import bearcart
import pandas as pd
import pandas.io.data as web

html_path = r'index.html'
data_path = r'data.json'
js_path = 'rickshaw.min.js'
css_path = 'rickshaw.min.css'

# All of the following import code comes from Wes McKinney's book, Python
# for Data Analysis

date_start = datetime.datetime(2010, 1, 1)
date_end = datetime.datetime(2014, 1, 1)
all_data = {ticker: web.DataReader(ticker, 'yahoo', date_start, date_end)
            for ticker in 'AAPL IBM YHOO MSFT'.split()}

price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.items()})

# Two data, line chart
df = pd.concat([price['YHOO'], price['MSFT']], axis=1)

vis = bearcart.Chart(df)
vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

# Bunch of data, area chart
vis = bearcart.Chart(price, plt_type='area')
vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

# Two data, custom colors, scatterplot
vis = bearcart.Chart(df, plt_type='scatterplot', colors={'AAPL': '#1d4e69',
                                                         'GOOG': '#3b98ca'})

vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

# -*- coding: utf-8 -*-
'''
An example for Bearcart
'''

import bearcart
import pandas as pd

html_path = r'index.html'
data_path = r'data.json'
js_path = 'rickshaw.min.js'
css_path = 'rickshaw.min.css'

#All of the following import code comes from Wes McKinney's book, Python
#for Data Analysis

import pandas.io.data as web

all_data = {}

for ticker in ['AAPL', 'GOOG', 'XOM', 'MSFT', 'INTC', 'YHOO']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2012', '1/1/2013')

price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.iteritems()})

#Two data, line chart
df = pd.concat([price['AAPL'], price['GOOG']], axis=1)

vis = bearcart.Chart(df)
vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

#Bunch of data, area chart
vis = bearcart.Chart(price, plt_type='area')
vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

#Two data, custom colors, scatterplot
vis = bearcart.Chart(df, plt_type='scatterplot', colors={'AAPL': '#1d4e69',
                                                         'GOOG': '#3b98ca' })

vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

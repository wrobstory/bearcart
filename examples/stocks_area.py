# -*- coding: utf-8 -*-
'''
An example for Bearcart
'''

import bearcart
import pandas as pd

html_path = r'index.html'
data_path = r'data.json'
js_path = r'rickshaw.min.js'
css_path = r'rickshaw.min.css'


#All of the following import code comes from Wes McKinney's book, Python 
#for Data Analysis

import pandas.io.data as web

all_data = {}

for ticker in ['AAPL', 'GOOG', 'FB', 'YHOO', 'MSFT', 'INTC']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2010', '1/1/2013')

price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.iteritems()})

vis = bearcart.Chart(price)
vis.create_chart(html_path=html_path, data_path=data_path, 
                 js_path=js_path, css_path=css_path)


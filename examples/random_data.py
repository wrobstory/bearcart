# -*- coding: utf-8 -*-
'''
An example for Bearcart
'''

import random
import bearcart
import pandas as pd

html_path = r'index.html'
data_path = r'data.json'
js_path = 'rickshaw.min.js'
css_path = 'rickshaw.min.css'

tabular_data_1 = [random.randint(10, 100) for x in range(0, 25, 1)]
tabular_data_2 = [random.randint(10, 100) for x in range(0, 25, 1)]
tabular_data_3 = [random.randint(10, 100) for x in range(0, 25, 1)]
df = pd.DataFrame({'Data 1': tabular_data_1, 'Data 2': tabular_data_2, 
                   'Data 3': tabular_data_3})

vis = bearcart.Chart(df, x_time=False)
vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

#Bunch of data, area chart
vis = bearcart.Chart(df, x_time=False, plt_type='area')
vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

#Bunch of data, bar chart
vis = bearcart.Chart(df, x_time=False, plt_type='bar')
vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

#Two data, custom colors, scatterplot
vis = bearcart.Chart(df, x_time=False, plt_type='scatterplot',
                     colors={'Data 1': '#1d4e69',
                             'Data 2': '#3b98ca',
                             'Data 3': '#04090d' })

vis.create_chart(html_path=html_path, data_path=data_path,
                 js_path=js_path, css_path=css_path)

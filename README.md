#Bearcart
![BearCart](http://farm9.staticflickr.com/8254/8711978179_4f3a42e2b8_o.jpg)
###Creating Rickshaw.js visualizations with Python Pandas

[Rickshaw.js](http://code.shutterstock.com/rickshaw/) is a great JavaScript library built on D3 by the folks at Shutterstock for plotting timeseries. [Pandas](http://pandas.pydata.org/) is a great Python library built by a number of outstanding folks in the open source community for creating timeseries. Bear, meet Cart. 

Concept
-------
Pandas Series and DataFrames with DatetimeIndex goes in. Rickshaw.js comes out. 

Bearcart is a small library for creating Rickshaw visualizations with Pandas timeseries data structures. It has a simple API, a number of plot types, and some really nice legends and tooltips thanks to the folks at Shutterstock.  

Bearcart uses Jinja2 templating to create the output, and the files are simple HTML/CSS/JS that can be manipulated after the fact for your application. 

Getting Started
---------------

Let's plot some stocks and make a line chart. Get data with Pandas, make visualization with Bearcart: 
```python
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

for ticker in ['AAPL', 'GOOG']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2010', '1/1/2013')

price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.iteritems()})

vis = bearcart.Chart(price)
vis.create_chart(html_path=html_path, data_path=data_path, 
                 js_path=js_path, css_path=css_path)
```

Go take a look at [this bl.ock](http://bl.ocks.org/wrobstory/5523221) for the interactive example with the tooltip and legend data selection. 

Lets try more companies, and an area plot: 
```python
all_data = {}
for ticker in ['AAPL', 'GOOG', 'XOM', 'MSFT', 'INTC', 'YHOO']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2012', '1/1/2013')
price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.iteritems()})

vis = bearcart.Chart(price, type='area')

```

Interactive version [here]. Finally, let's make a scatterplot with some custom colors: 
```python
df = pd.concat([price['AAPL'], price['GOOG']], axis=1)[:100]

vis = bearcart.Chart(df, type='scatterplot', colors={'AAPL': '#1d4e69', 
                                                     'GOOG': '#3b98ca' })
```

Interactive example [here].

If you don't want some of the chart features, like the legend, hover, x-axis, etc, you can just pass those parameters as false when defining the chart: 
```python
vis = bearcart.Chart(df, hover=False, legend=False)



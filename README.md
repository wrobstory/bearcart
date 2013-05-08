#Bearcart
![BearCart](http://farm9.staticflickr.com/8254/8711978179_4f3a42e2b8_o.jpg)
###Creating Rickshaw.js visualizations with Python Pandas

[Rickshaw.js](http://code.shutterstock.com/rickshaw/) is a great JavaScript library built on D3 by the folks at Shutterstock for plotting timeseries. [Pandas](http://pandas.pydata.org/) is a great Python library built by a number of outstanding folks in the open source community for creating timeseries. Bear, meet Cart. 

Concept
-------
Pandas Series and DataFrames with DatetimeIndex goes in. Rickshaw.js comes out. 

Bearcart is a small library for creating Rickshaw visualizations with Pandas timeseries data structures. It has a simple API, a number of plot types, and some really nice legends and tooltips thanks to the folks at Shutterstock.  

Bearcart uses Jinja2 templating to create the output, and the files are simple HTML/CSS/JS that can be manipulated after the fact for your application. 

Installation
------------
```shell
$ pip install bearcart
```

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
![Line](http://farm9.staticflickr.com/8274/8712121301_7b2c09a6eb_z.jpg)

Go take a look at [this bl.ock](http://bl.ocks.org/wrobstory/5523221) for the interactive example with the tooltip and legend data selection. 

Lets try more companies, and an area plot: 
```python
all_data = {}
for ticker in ['AAPL', 'GOOG', 'XOM', 'MSFT', 'INTC', 'YHOO']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2012', '1/1/2013')
price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.iteritems()})

vis = bearcart.Chart(price, plt_type='area')

```
![Area](http://farm9.staticflickr.com/8271/8712121307_5204f670ea_z.jpg)

Interactive version [here](http://bl.ocks.org/wrobstory/5523345). Finally, let's make a scatterplot with some custom colors: 
```python
df = pd.concat([price['AAPL'], price['GOOG']], axis=1)[:100]

vis = bearcart.Chart(df, plt_type='scatterplot', colors={'AAPL': '#1d4e69', 
                                                         'GOOG': '#3b98ca' })
```
![Scatter](http://farm9.staticflickr.com/8140/8712121243_4a643185d8_z.jpg)

Interactive example [here](http://bl.ocks.org/wrobstory/5523361).

If you don't want some of the chart features, like the legend, hover, x-axis, etc, you can just pass those parameters as false when defining the chart: 
```python
vis = bearcart.Chart(df, hover=False, legend=False)
```

Bearcart also supports non-timeseries plotting. Just pass ```x_time=False```:
```python
vis = bearcart.Chart(df, plt_type='bar', x_time=False)
vis = bearcart.Chart(df, plt_type='area', x_time=False)
```
![Bar](http://farm8.staticflickr.com/7284/8719891356_fd1e5a49fd_z.jpg)
![Area](http://farm8.staticflickr.com/7314/8719891050_1659241cdf_z.jpg)

That's it- a small little library for making nice little interactive timeseries charts. Happy plotting!

Dependencies
---------------
Pandas

Jinja2

Status
-------
Beta, at least until it gets some use. 

Docs
----
You can read the entire source in 20 minutes. But I needed to learn Sphinx: https://bearcart.readthedocs.org



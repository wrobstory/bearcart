Getting Started
================================================================

Let's plot some stocks and make a line chart. Get data with Pandas, make visualization with Bearcart::

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


Go take a look at `this bl.ock <http://bl.ocks.org/wrobstory/5523221>`_ for the interactive example with the tooltip and legend data selection. 

Lets try more companies, and an area plot::

    all_data = {}
    for ticker in ['AAPL', 'GOOG', 'XOM', 'MSFT', 'INTC', 'YHOO']:
        all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2012', '1/1/2013')
    price = pd.DataFrame({tic: data['Adj Close']
                          for tic, data in all_data.iteritems()})

    vis = bearcart.Chart(price, plt_type='area')

Interactive version `here <http://bl.ocks.org/wrobstory/5523345>`_. Finally, let's make a scatterplot with some custom colors::

    df = pd.concat([price['AAPL'], price['GOOG']], axis=1)[:100]

    vis = bearcart.Chart(df, plt_type='scatterplot', colors={'AAPL': '#1d4e69', 
                                                             'GOOG': '#3b98ca' })

Interactive example `here <http://bl.ocks.org/wrobstory/5523361>`_

If you don't want some of the chart features, like the legend, hover, x-axis, etc, you can just pass those parameters as false when defining the chart::

    vis = bearcart.Chart(df, hover=False, legend=False)

That's it- a small little library for making nice little interactive timeseries charts. Happy plotting!
.. bearcart documentation master file

Bearcart: Creating Rickshaw.js visualizations with Python Pandas
================================================================

`Rickshaw.js <http://code.shutterstock.com/rickshaw/>`_ is a great JavaScript library built on D3 by the folks at Shutterstock for plotting timeseries. `Pandas <http://pandas.pydata.org/>`_ is a great Python library built by a number of outstanding folks in the open source community for creating timeseries. Bear, meet Cart. 

Concept
^^^^^^^^
Pandas Series and DataFrames with DatetimeIndex goes in. Rickshaw.js comes out. 

Bearcart is a small library for creating Rickshaw visualizations with Pandas timeseries data structures. It has a simple API, a number of plot types, and some really nice legends and tooltips thanks to the folks at Shutterstock.  

Bearcart uses Jinja2 templating to create the output, and the files are simple HTML/CSS/JS that can be manipulated after the fact for your application. 

Contents:

.. toctree::
   :maxdepth: 2

   Getting Started <gettingstarted>

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`


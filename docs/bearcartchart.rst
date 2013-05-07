Bearcart.Chart
================================================================
Generate a Rickshaw time series visualization with Pandas
Series and DataFrames.

The bearcart Chart generates the Rickshaw visualization of a Pandas
timeseries Series or DataFrame. The only required parameters are
data, width, height, and type. Colors is an optional parameter;
bearcart will default to the Rickshaw spectrum14 color palette if
none are passed. Keyword arguments can be passed to disable the
following components:
   * x_axis
   * y_axis
   * hover
   * legend

.. autoclass:: bearcart.Chart
   :members:
# -*- coding: utf-8 -*-
'''
Rickshaw
-------

Python Pandas + Rickshaw.js

'''

from __future__ import print_function
from __future__ import division

from collections import defaultdict
import json
import os
import time
from uuid import uuid4
import sys

from jinja2 import Environment, PackageLoader
import pandas as pd
from pkg_resources import resource_string
import numpy as np

from ._compat import iteritems

ENV = Environment(loader=PackageLoader('bearcart', 'templates'))

def initialize_notebook():
    """Initialize the IPython notebook display elements"""
    try:
        from IPython.core.display import display, HTML
    except ImportError:
        print("IPython Notebook could not be loaded.")

    lib_js = ENV.get_template('ipynb_init_js.html')
    lib_css = ENV.get_template('ipynb_init_css.html')

    display(HTML(lib_js.render()))
    display(HTML(lib_css.render()))

class Chart(object):

    '''Visualize Pandas Timeseries with Rickshaw.js'''

    def __init__(self, data=None, width=750, height=400, plt_type='line',
                 colors=None, x_time=True, y_zero=False, **kwargs):
        '''Generate a Rickshaw time series visualization with Pandas
        Series and DataFrames.

         The bearcart Chart generates the Rickshaw visualization of a Pandas
         timeseries Series or DataFrame. The only required parameters are
         data, width, height, and type. Colors is an optional parameter;
         bearcart will default to the Rickshaw spectrum14 color palette if
         none are passed. Keyword arguments can be passed to disable the
         following components:
            - x_axis
            - y_axis
            - hover
            - legend
            - slider

        Parameters
        ----------
        data: Pandas Series or DataFrame, default None
             The Series or Dataframe must have a Datetime index.
        width: int, default 960
            Width of the chart in pixels
        height: int, default 500
            Height of the chart in pixels
        plt_type: string, default 'line'
            Must be one of 'line', 'area', 'scatterplot' or 'bar'
        colors: dict, default None
            Dict with keys matching DataFrame or Series column names, and hex
            strings for colors
        x_time: boolean, default True
            If passed as False, the x-axis will have non-time values
        y_zero: boolean, default False
            The y-axis defaults to auto scaling. Pass True to set the min
            y-axis value to 0.
        kwargs:
            Keyword arguments that, if passed as False, will disable the
            following components: x_axis, y_axis, hover, legend, slider

        Returns
        -------
        Bearcart object

        Examples
        --------
        >>>vis = bearcart.Chart(data=df, width=800, height=300, type='area')
        >>>vis = bearcart.Chart(data=series,type='scatterplot',
                                colors={'Data 1': '#25aeb0',
                                        'Data 2': '#114e4f'})
        #Disable x_axis and legend
        >>>vis = bearcart.Chart(data=df, x_axis=False, legend=False)

        '''
        self.chart_id = '_'.join(['bearcart', uuid4().hex])

        self.defaults = {'x_axis': True, 'y_axis': True, 'hover': True,
                         'legend': True, 'slider': True}

        self.env = ENV

        # Colors need to be js strings
        if colors:
            self.colors = {key: "'{0}'".format(value)
                           for key, value in iteritems(colors)}
        else:
            self.colors = None

        self.x_axis_time = x_time
        self.renderer = plt_type
        self.width = width
        self.height = height
        self.y_zero = y_zero
        self.template_vars = {}

        # Update defaults for passed kwargs
        for key, value in iteritems(kwargs):
            self.defaults[key] = value

        for id_var in ['y_axis_id', 'legend_id', 'slider_id']:
            id = '_'.join(['bearcart', id_var, uuid4().hex])
            setattr(self, id_var, id)

        # Get templates for graph elements
        for att, val in iteritems(self.defaults):
            render_vars = {}
            if val:
                if not self.x_axis_time:
                    if att == 'x_axis':
                        att = 'x_axis_num'
                    elif att == 'hover':
                        render_vars = {'x_hover': 'xFormatter: function(x)'
                                       '{return Math.floor(x / 10) * 10}'}
                render_vars.update({'height': self.height,
                                    'chart_id': self.chart_id,
                                    'y_axis_id': self.y_axis_id,
                                    'legend_id': self.legend_id,
                                    'slider_id': self.slider_id})
                temp = self.env.get_template(att + '.js')
                self.template_vars.update({att: temp.render(render_vars)})

        # Transform data into Rickshaw-happy JSON format
        if data is not None:
            self.transform_data(data)

    def transform_data(self, data):
        '''Transform Pandas Timeseries into JSON format

        Parameters
        ----------
        data: DataFrame or Series
            Pandas DataFrame or Series must have datetime index

        Returns
        -------
        JSON to object.json_data

        Example
        -------
        >>>vis.transform_data(df)
        >>>vis.json_data

        '''

        def type_check(value):
            '''Type check values for JSON serialization. Native Python JSON
            serialization will not recognize some Numpy data types properly,
            so they must be explictly converted.'''
            if pd.isnull(value):
                return None
            elif (isinstance(value, pd.tslib.Timestamp) or
                  isinstance(value, pd.Period)):
                return time.mktime(value.timetuple())
            elif isinstance(value, (int, np.integer)):
                return int(value)
            elif isinstance(value, (float, np.float_)):
                return float(value)
            elif isinstance(value, str):
                return str(value)
            else:
                return value

        objectify = lambda dat: [{"x": type_check(x), "y": type_check(y)}
                                 for x, y in iteritems(dat)]

        self.raw_data = data
        if isinstance(data, pd.Series):
            data.name = data.name or 'data'
            self.json_data = [{'name': data.name, 'data': objectify(data)}]
        elif isinstance(data, pd.DataFrame):
            self.json_data = [{'name': x[0], 'data': objectify(x[1])}
                              for x in iteritems(data)]

    def _build_graph(self):
        '''Build Rickshaw graph syntax with all data'''

        # Set palette colors if necessary
        if not self.colors:
            self.palette = self.env.get_template('palette.js')
            self.template_vars.update({'palette': self.palette.render()})
            self.colors = {x['name']: 'palette.color()' for x in self.json_data}

        template_vars = []
        for index, dataset in enumerate(self.json_data):
            group = 'datagroup' + str(index)
            template_vars.append({'name': str(dataset['name']),
                                  'color': self.colors[dataset['name']],
                                  'data': 'json[{0}].data'.format(index)})

        variables = {'dataset': template_vars, 'width': self.width,
                     'height': self.height, 'render': self.renderer,
                     'chart_id': self.chart_id}
        if not self.y_zero:
            variables.update({'min': "min: 'auto',"})

        graph = self.env.get_template('graph.js')
        self.template_vars.update({'graph': graph.render(variables)})

    def create_chart(self, html_path='index.html', data_path='data.json',
                     js_path='rickshaw.min.js', css_path='rickshaw.min.css',
                     html_prefix=''):
        '''Save bearcart output to HTML and JSON.

        Parameters
        ----------
        html_path: string, default 'index.html'
            Path for html output
        data_path: string, default 'data.json'
            Path for data JSON output
        js_path: string, default 'rickshaw.min.js'
            If passed, the Rickshaw javascript library will be saved to the
            path. The file must be named "rickshaw.min.js"
        css_path: string, default 'rickshaw.min.css'
            If passed, the Rickshaw css library will be saved to the
            path. The file must be named "rickshaw.min.css"
        html_prefix: Prefix path to be appended to all the other paths for file
            creation, but not in the generated html file. This is needed if the
            html file does not live in the same folder as the running python
            script.

        Returns
        -------
        HTML, JSON, JS, and CSS

        Example
        --------
        >>>vis.create_chart(html_path='myvis.html', data_path='visdata.json'),
                            js_path='rickshaw.min.js',
                            cs_path='rickshaw.min.css')
        '''

        self.template_vars.update({'data_path': str(data_path),
                                   'js_path': js_path,
                                   'css_path': css_path,
                                   'chart_id': self.chart_id,
                                   'y_axis_id': self.y_axis_id,
                                   'legend_id': self.legend_id,
                                   'slider_id': self.slider_id})

        self._build_graph()
        html = self.env.get_template('bcart_template.html')
        self.HTML = html.render(self.template_vars)

        with open(os.path.join(html_prefix, html_path), 'w') as f:
            f.write(self.HTML)

        with open(os.path.join(html_prefix, data_path), 'w') as f:
            json.dump(self.json_data, f, sort_keys=True, indent=4,
                      separators=(',', ': '))

        if js_path:
            js = resource_string('bearcart', 'rickshaw.min.js')
            with open(os.path.join(html_prefix, js_path), 'w') as f:
                f.write(js)
        if css_path:
            css = resource_string('bearcart', 'rickshaw.min.css')
            with open(os.path.join(html_prefix, css_path), 'w') as f:
                    f.write(css)

    def _repr_html_(self):
        """Build the HTML representation for IPython."""
        self.chart_id = '_'.join(['bearcart', uuid4().hex])
        self.template_vars.update({'chart_id': self.chart_id,
                                   'y_axis_id': self.y_axis_id,
                                   'legend_id': self.legend_id,
                                   'slider_id': self.slider_id,
                                   'export_json': json.dumps(self.json_data)})

        self._build_graph()
        html = self.env.get_template('ipynb_repr.html')
        return html.render(self.template_vars)

    def display(self):
        """Display the visualization inline in the IPython notebook.

        This is deprecated, use the following instead::

            from IPython.display import display
            display(viz)
        """
        from IPython.core.display import display, HTML
        display(HTML(self._repr_html_()))


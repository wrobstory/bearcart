# -*- coding: utf-8 -*-
'''
Rickshaw
-------

Python Pandas + Rickshaw.js

'''

from __future__ import print_function
from __future__ import division
import time
import json
import os
from collections import defaultdict
from pkg_resources import resource_string
import pandas as pd
from jinja2 import Environment, PackageLoader


class Chart(object):
    '''Visualize Pandas Timeseries with Rickshaw.js'''

    def __init__(self, data=None, width=750, height=400, plt_type='line',
                 colors=None, x_time=True, **kwargs):
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

        Parameters
        ----------
        data: Pandas Series or DataFrame, default None
             The Series or Dataframe must have a Datetime index.
        width: int, default 960
            Width of the chart in pixels
        height: int, default 500
            Height of the chart in pixels
        type: string, default 'line'
            Must be one of 'line', 'area', 'scatterplot' or 'bar'
        colors: dict, default None
            Dict with keys matching DataFrame or Series column names, and hex
            strings for colors
        x_time: boolean, default True
            If passed as False, the x-axis will have non-time values
        kwargs:
            Keyword arguments that, if passed as False, will disable the
            following components: x_axis, y_axis, hover, legend

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

        self.defaults = {'x_axis': True, 'y_axis': True, 'hover': True,
                         'legend': True}

        self.env = Environment(loader=PackageLoader('bearcart', 'templates'))

        #Colors need to be js strings
        if colors:
            self.colors = {key: "'{0}'".format(value)
                           for key, value in colors.iteritems()}
        else:
            self.colors = None

        self.x_axis_time = x_time
        self.renderer = plt_type
        self.width = width
        self.height = height
        self.template_vars = {}

        #Update defaults for passed kwargs
        for key, value in kwargs.iteritems():
            self.defaults[key] = value

        #Get templates for graph elements
        for att, val in self.defaults.iteritems():
            render_vars = {}
            if val:
                if not self.x_axis_time:
                    if att == 'x_axis':
                        att = 'x_axis_num'
                    elif att == 'hover':
                        render_vars = {'x_hover': 'xFormatter: function(x)'
                                       '{return Math.floor(x / 10) * 10}'}
                temp = self.env.get_template(att + '.js')
                self.template_vars.update({att: temp.render(render_vars)})

        #Transform data into Rickshaw-happy JSON format
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

        objectify = lambda dat: [{"x": x, "y": y} for x, y in dat.iteritems()]

        self.raw_data = data
        if isinstance(data, pd.Series):
            data.name = data.name or 'data'
            self.json_data = [{'name': data.name, 'data': objectify(data)}]
        elif isinstance(data, pd.DataFrame):
            self.json_data = [{'name': x[0], 'data': objectify(x[1])}
                              for x in data.iteritems()]

        #Transform to Epoch seconds for Rickshaw
        if self.x_axis_time: 
            for datacol in self.json_data:
                datacol = datacol['data']
                for objs in datacol:
                    if pd.isnull(objs['x']):
                        objs['x'] = None
                    elif (isinstance(objs['x'], pd.tslib.Timestamp) or
                          isinstance(objs['x'], pd.Period)):
                        objs['x'] = time.mktime(objs['x'].timetuple())

    def _build_graph(self):
        '''Build Rickshaw graph syntax with all data'''

        #Set palette colors if necessary
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
                     'height': self.height, 'render': self.renderer}
        graph = self.env.get_template('graph.js')
        self.template_vars.update({'graph': graph.render(variables)})

    def create_chart(self, html_path='index.html', data_path='data.json',
                     js_path=None, css_path=None):
        '''Save bearcart output to HTML and JSON.

        Parameters
        ----------
        html_path: string, default 'index.html'
            Path for html output
        data_path: string, default 'data.json'
            Path for data JSON output
        js_path: string, default None
            If passed, the Rickshaw javascript library will be saved to the
            path. The file must be named "rickshaw.min.js"
        css_path: string, default None
            If passed, the Rickshaw css library will be saved to the
            path. The file must be named "rickshaw.min.css"

        Returns
        -------
        HTML, JSON, JS, and CSS

        Example
        --------
        >>>vis.create_chart(html_path='myvis.html', data_path='visdata.json'),
                            js_path='rickshaw.min.js',
                            cs_path='rickshaw.min.css')
        '''

        self.template_vars.update({'data_path': str(data_path)})

        self._build_graph()
        html = self.env.get_template('bcart_template.html')
        self.HTML = html.render(self.template_vars)

        with open(html_path, 'w') as f:
            f.write(self.HTML)

        with open(data_path, 'w') as f:
            json.dump(self.json_data, f, sort_keys=True, indent=4,
                      separators=(',', ': '))

        if js_path:
            js = resource_string('bearcart', 'rickshaw.min.js')
            with open(js_path, 'w') as f:
                f.write(js)
        if css_path:
            css = resource_string('bearcart', 'rickshaw.min.css')
            with open(css_path, 'w') as f:
                    f.write(css)

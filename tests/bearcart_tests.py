  # -*- coding: utf-8 -*-
'''
Test Bearcart
---------

'''
from __future__ import print_function
from __future__ import division

import datetime
import time
import random

import pandas as pd
import pandas.io.data as web
from pandas.util.testing import assert_almost_equal
from jinja2 import Environment, FileSystemLoader
import nose.tools as nt

import bearcart


class testBearcart(object):
    '''Test Bearcart Chart class'''

    @classmethod
    def setup_class(self):

        all_data = {}
        date_start = datetime.datetime(2010, 1, 1)
        date_end = datetime.datetime(2014, 1, 1)
        for ticker in ['AAPL', 'MSFT']:
            all_data[ticker] = web.DataReader(ticker, 'yahoo', date_start,
                                              date_end)
        self.price = pd.DataFrame({tic: data['Adj Close']
                                   for tic, data in all_data.items()})
        self.templates = Environment(loader=FileSystemLoader('templates'))

    def test_init(self):
        #Test defaults
        chart = bearcart.Chart(colors={'Data 1': '#25aeb0'})
        assert chart.height == 400
        assert chart.width == 750
        assert chart.renderer == 'line'
        assert chart.colors == {'Data 1': "'#25aeb0'"}
        temps = {x.split('.')[0]: x.split('.')[1]
                 for x in self.templates.list_templates()}
        for key, value in chart.template_vars.iteritems():
            template = self.templates.get_template('.'.join([key, temps[key]]))
            assert value == template.render()

    def test_params(self):
        #Test params
        chart = bearcart.Chart(width=500, height=1000, plt_type='area')
        assert chart.height == 1000
        assert chart.width == 500
        assert chart.renderer == 'area'

        #Test component removal
        chart = bearcart.Chart(x_axis=False, legend=False)
        nt.assert_list_equal(chart.template_vars.keys(),
                             ['y_axis', 'hover', 'slider'])

    def test_data(self):
        #Test data
        series = self.price['AAPL']
        chart = bearcart.Chart(series)
        assert_almost_equal(chart.raw_data, series)
        assert chart.json_data[0]['name'] == 'AAPL'
        assert len(series) == len(chart.json_data[0]['data'])
        nt.eq_(time.mktime(series.index[0].timetuple()),
               chart.json_data[0]['data'][0]['x'])


    def test_non_timeseries(self):
        tabular_data = [random.randint(10, 100) for x in range(0, 25, 1)]
        df = pd.DataFrame({'Data 1': tabular_data})

        chart = bearcart.Chart(df, x_time=False)
        nt.assert_in('x_axis_num', chart.template_vars)
        nt.assert_in('xFormatter: function(x)'
                     '{return Math.floor(x / 10) * 10}\n}',
                     chart.template_vars['hover'])

    def test_build_graph(self):
        series = self.price['AAPL']
        chart = bearcart.Chart(series)
        chart._build_graph()

        vars = {'dataset': [{'name': 'AAPL', 'color': 'palette.color()',
                            'data': 'json[0].data', }],
                'width': 750, 'height': 400, 'render': 'line',
                'min': "min: 'auto',"}

        graph_templ = self.templates.get_template('graph.js')
        graph = graph_templ.render(vars)

        import ipdb;ipdb.set_trace()

        assert chart.colors == {'AAPL': 'palette.color()'}
        assert chart.template_vars['graph'] == graph










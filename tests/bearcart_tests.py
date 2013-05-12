  # -*- coding: utf-8 -*-
'''
Test Bearcart
---------

'''
from __future__ import print_function
from __future__ import division
import time
import random
import bearcart
import pandas as pd
from pandas.util.testing import assert_almost_equal
from jinja2 import Environment, FileSystemLoader
import nose.tools as nt


class testBearcart(object):
    '''Test Bearcart Chart class'''

    @classmethod
    def setup_class(self):
        '''Bearcart test data and template setup'''
        import pandas.io.data as web

        all_data = {}
        for ticker in ['AAPL', 'GOOG']:
            all_data[ticker] = web.get_data_yahoo(ticker,
                                                  '4/1/2013', '5/1/2013')
        self.price = pd.DataFrame({tic: data['Adj Close']
                                  for tic, data in all_data.iteritems()})
        self.templates = Environment(loader=FileSystemLoader('templates'))

    def test_init(self):
        '''Test bearcart chart creation'''

        #Test defaults
        chart = bearcart.Chart()
        assert chart.height == 400
        assert chart.width == 750
        assert chart.renderer == 'line'
        temps = {x.split('.')[0]: x.split('.')[1]
                 for x in self.templates.list_templates()}
        for key, value in chart.template_vars.iteritems():
            template = self.templates.get_template('.'.join([key, temps[key]]))
            assert value == template.render()

    def test_params(self):
        '''Test bearcart chart parameters and component removal'''

        #Test params
        chart = bearcart.Chart(width=500, height=1000, plt_type='area')
        assert chart.height == 1000
        assert chart.width == 500
        assert chart.renderer == 'area'

        #Test component removal
        chart = bearcart.Chart(x_axis=False, legend=False)
        nt.assert_list_equal(chart.template_vars.keys(),
                             ['y_axis', 'hover'])

    def test_data(self):
        '''Test bearcart data import and transformation'''

        #Test data
        series = self.price['AAPL']
        chart = bearcart.Chart(series)
        assert_almost_equal(chart.raw_data, series)
        assert chart.json_data[0]['name'] == 'AAPL'
        assert len(series) == len(chart.json_data[0]['data'])
        nt.eq_(time.mktime(series.index[0].timetuple()),
               chart.json_data[0]['data'][0]['x'])

    def test_non_timeseries(self):
        '''Test non timeseries data'''
        tabular_data = [random.randint(10, 100) for x in range(0, 25, 1)]
        df = pd.DataFrame({'Data 1': tabular_data})

        chart = bearcart.Chart(df, x_time=False)
        nt.assert_in('x_axis_num', chart.template_vars)
        nt.assert_in('xFormatter: function(x)'
                     '{return Math.floor(x / 10) * 10}\n}',
                     chart.template_vars['hover'])

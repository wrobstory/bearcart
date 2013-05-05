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
from collections import defaultdict
import pandas as pd
from jinja2 import Environment, PackageLoader
import pdb


class Cart(object): 
    '''Visualize Pandas Timeseries with Rickshaw.js'''
    
    def __init__(self, data=None, width=None, height=None, colors=None,
                  type='line', **kwargs):
        '''Generate a Rickshaw visualization with Pandas Timeseries'''
        
        self.env = Environment(loader=PackageLoader('bearcart', 'templates'))
        self.renderer = type
        self.colors = colors
        self.width = width or 550
        self.height = height or 250
        self.template_vars = {}
        
        if data is not None: 
            self.transform_data(data)
        
    def transform_data(self, data): 
        '''Transform Pandas Timeseries into JSON format'''
        
        objectify= lambda dat: [{"x": x, "y": y} for x, y in dat.iteritems()]
            
        self.raw_data = data
        if isinstance(data, pd.Series):
            data.name = data.name or 'data'
            self.json_data = [{'name': data.name, 'data': objectify(data)}]
        elif isinstance(data, pd.DataFrame): 
            self.json_data = [{'name': x[0], 'data': objectify(x[1])} 
                              for x in data.iteritems()]
          
        #Transform to Epoch time for JS                   
        for datacol in self.json_data:
            datacol = datacol['data']
            for objs in datacol: 
                if pd.isnull(objs['x']):
                    objs['x'] = None
                elif (isinstance(objs['x'], pd.tslib.Timestamp) or
                      isinstance(objs['x'], pd.Period)):
                    objs['x'] = time.mktime(objs['x'].timetuple())*1000
                    
    def _build_graph(self): 
        '''Build Rickshaw graph syntax'''
        if not self.colors: 
            self.palette = self.env.get_template('palette.js')
            self.template_vars.update({'palette': self.palette.render()})
            self.color = {x['name']: 'palette.color()' for x in self.json_data}
            
        template_vars = []
        for index, dataset in enumerate(self.json_data):
            group = 'datagroup' + str(index)
            template_vars.append({'name': str(dataset['name']),
                                  'color': self.color[dataset['name']],
                                  'data': 'json[{0}].data'.format(index)})
        
        variables = {'dataset': template_vars, 'width': self.width,
                     'height': self.height, 'render': self.renderer}                        
        graph = self.env.get_template('graph.js')
        self.template_vars.update({'graph': graph.render(variables)})
        
    def _build_all(self): 
        '''Build all components'''
        self._build_graph()
                       
    def create_chart(self, html_path=None, data_path=None):
        '''Save output to HTML and JSON'''
        
        self.template_vars.update({'data_path': str(data_path)})
        
        self._build_all()
        html = self.env.get_template('cart_template.html')
        self.HTML = html.render(self.template_vars)
        
        with open(html_path, 'w') as f: 
            f.write(self.HTML)
            
        with open(data_path, 'w') as f: 
            json.dump(self.json_data, f)

        
 
            
        
    
    
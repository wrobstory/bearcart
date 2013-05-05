# -*- coding: utf-8 -*-
'''
Rickshaw
-------

Python Pandas + Rickshaw.js

'''

from __future__ import print_function
from __future__ import division
from jinja2 import Template
from pkg_resources import resource_string

baseline = Template(resource_string('bearcart', 'cart_template.html'))

palette = 'var palette = new Rickshaw.Color.Palette();'

graph = Template('''
          var graph = new Rickshaw.Graph( {
                element: document.querySelector("#chart"),
                width: {{ width }},
                height: {{ height}},
                series: {{ data }}
                })''')

x_axis = 'var x_axis = new Rickshaw.Graph.Axis.Time( { graph: graph } );'

y_axis = Template('''
var y_axis = new Rickshaw.Graph.Axis.Y( {
        graph: graph,
        orientation: 'left',
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        element: document.getElementById('y_axis'),
} );''')

css = Template('''
          #chart_container {
                position: relative;
                font-family: Arial, Helvetica, sans-serif;
          }
          #chart {
                  position: relative;
                  left: 40px;
          }
          #y_axis {
                  position: absolute;
                  top: 0;
                  bottom: 0;
                  width: 40px;
          }''')
               



    
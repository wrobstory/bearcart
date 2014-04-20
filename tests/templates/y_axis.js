var y_axis = new Rickshaw.Graph.Axis.Y( {
        graph: graph,
        orientation: 'left',
        height: {{ height }},
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        element: d3.select("#{{ y_axis_id }}").node()
} );

var legend = new Rickshaw.Graph.Legend({
    graph: graph,
    element: d3.select("#{{ legend_id }}").node()

});

var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
    graph: graph,
    legend: legend
});

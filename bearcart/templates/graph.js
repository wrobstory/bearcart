var graph = new Rickshaw.Graph( {
                element: document.querySelector("#chart"),
                {{ min }}
                width: {{ width }},
                height: {{ height}},
                renderer: '{{ render }}',
                series: [{% for data in dataset : %}
                         {name: '{{ data['name'] }}',
                          color: {{ data['color'] }},
                          data: {{ data['data'] }}}{% if not loop.last %},{% endif %}
                          {% endfor %}]
                })
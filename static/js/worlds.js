var default_title = 'Grade One';
var default_grade;
var curr_grade = '1';
var state = true;
var graphs;
var graph_title;

var graph_data = [{
        x: "",
        y: "",
        type: 'bar'
    }];


var bar_layout = {
        title: default_title,

        xaxis: {
            tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
            }
        },
        yaxis: {
            title: 'Number of Wins',
            titlefont: {
                size: 16,
                color: 'rgb(107, 107, 107)'
            },
            tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
            }
        },
        legend: {
            x: 0,
            y: 1.0,
            bgcolor: 'rgba(255, 255, 255, 0)',
            bordercolor: 'rgba(255, 255, 255, 0)'
        },
        height: 700,
        width: 1000,
        margin: {
            l: 50,
            r: 50,
            b: 250,
            t: 50,
            pad: 4
        },

    };

function create_worlds_graph(new_graphs, graph_title) {
    graphs = new_graphs;
    default_title = graph_title;
    bar_layout['title'] = graph_title;
    graph_data[0]['x'] = new_graphs[0];
    graph_data[0]['y'] = new_graphs[1];
    Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud: true});
}

$('#ddselect button').on('click', function() {
    default_grade = $(this).text();
    if(default_grade !== curr_grade) {
        curr_grade = default_grade;
        $.getJSON($SCRIPT_ROOT + '/_get_worlds_data', {
            grade: String(default_grade),
            place: '1'
        }, function (data) {
            graph_title = String(data[0]);
            $('#worlds_table').removeClass("table-striped table-bordered table-hover");
            if(default_grade !== '1') {
                $('#worlds_table').html("");
                $('#worlds_table').append("<thead class=\"thead-dark\">\n" +
                    "                        <tr>\n" +
                    "                            <th scope=\"col\">Year</th>\n" +
                    "                            <th scope=\"col\">Grade</th>\n" +
                    "                            <th scope=\"col\">Competition</th>\n" +
                    "                            <th scope=\"col\">Winning Band</th>\n" +
                    "                            <th scope=\"col\">Overall Total</th>\n" +
                    "                        </tr>\n" +
                    "                    </thead>")
                for (var i = 0; i < data[1].length; i++) {
                    var row = data[1][i];
                    var row_td = "";
                    for(var k = 0; k < row.length; k++){
                        row_td += "<td>"+ row[k] +"</td>"
                    }
                    $('#worlds_table').append("<tr>" + row_td + "</tr>");
                }
            }
            else{
                $('#worlds_table').html("");
                $('#worlds_table').append("<thead class=\"thead-dark\">\n" +
                    "                        <tr>\n" +
                    "                            <th scope=\"col\">Year</th>\n" +
                    "                            <th scope=\"col\">Grade</th>\n" +
                    "                            <th scope=\"col\">Competition</th>\n" +
                    "                            <th scope=\"col\">Winning Band</th>\n" +
                    "                            <th scope=\"col\">Medley Total</th>\n" +
                    "                            <th scope=\"col\">MSR Total</th>\n" +
                    "                            <th scope=\"col\">Overall Total</th>\n" +
                    "                        </tr>\n" +
                    "                    </thead>")
                for (var i = 0; i < data[1].length; i++) {
                    var row = data[1][i];
                    var row_td = "";
                    for(var k = 0; k < row.length; k++){
                        row_td += "<td>"+ row[k] +"</td>"
                    }
                    $('#worlds_table').append("<tr>" + row_td + "</tr>");
                }
            }
            $('#worlds_table').addClass("table-striped table-bordered table-hover");
        });

        $.getJSON($SCRIPT_ROOT + '/_get_worlds_total', {
            grade: String(default_grade),
            place: '1'
        }, function (data) {
            graphs = data;
            graph_data = [{
                x: graphs[0],
                y: graphs[1],
                type: 'bar'
            }];
            bar_layout['title'] = graph_title;
            Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud: true});
        });
    }
});
var default_grade = '1';
var default_title = 'Grade One';
var default_type = 'w';
var state = true;

var graph_data = [{
        x: "",
        y: "",
        type: 'bar'
    }];

var pie_layout = {
        title: default_title,
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

function create_totals_graph(graphs, graph_title) {

    bar_layout['title'] = graph_title;
    graph_data[0]['x'] = graphs[0];
    graph_data[0]['y'] = graphs[1];
    Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud: true});
}

$('#ddselect button').on('click', function() {
    default_grade = $(this).text();

    console.log(default_type);

    if(default_type === 'w'){
        $.getJSON($SCRIPT_ROOT + '/_get_new_title', {
            grade: String(default_grade),
            place: '1'
        }, function (data) {
            graph_title = String(data)
        });

        $.getJSON($SCRIPT_ROOT + '/_get_grade_total', {
            grade: String(default_grade),
            place: '1'
        }, function (data) {
            graphs = data;
            if(state){
            graph_data = [{
                x: graphs[0],
                y: graphs[1],
                type: 'bar'
            }];
            bar_layout['title'] = graph_title;
            pie_layout['title'] = graph_title;
            Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
            }
            else{
            graph_data = [{
                labels: graphs[0],
                values: graphs[1],
                type: 'pie'
            }];
            bar_layout['title'] = graph_title;
            pie_layout['title'] = graph_title;
            Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
            }
        });
    }
    else{
        $.getJSON($SCRIPT_ROOT + '/_get_new_place_title', {
            grade: String(default_grade),
            place: '1',
            type: default_type,
        }, function (data) {
            graph_title = String(data)
        });

        $.getJSON($SCRIPT_ROOT + '/_get_grade_place_total', {
            grade: String(default_grade),
            place: '1',
            type: default_type
        }, function (data) {
            graphs = data;
            if(!state){
            graph_data = [{
                x: graphs[0],
                y: graphs[1],
                type: 'bar'
            }];
            bar_layout['title'] = graph_title;
            pie_layout['title'] = graph_title;
            Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
            }
            else{
            graph_data = [{
                labels: graphs[0],
                values: graphs[1],
                type: 'pie'
            }];
            bar_layout['title'] = graph_title;
            pie_layout['title'] = graph_title;
            Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
            }
        });
    }
});

$('#wins_tog').on('click', function() {
    default_type = 'w';
    $.getJSON($SCRIPT_ROOT + '/_get_new_title', {
        grade: String(default_grade),
        place: '1'
    }, function (data) {
        graph_title = String(data)
    });

    $.getJSON($SCRIPT_ROOT + '/_get_grade_total', {
        grade: String(default_grade),
        place: '1'
    }, function (data) {
        graphs = data;
        if(state){
        graph_data = [{
            x: graphs[0],
            y: graphs[1],
            type: 'bar'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
        }
        else{
        graph_data = [{
            labels: graphs[0],
            values: graphs[1],
            type: 'pie'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
    }
    });
});

$('#piping_tog').on('click', function() {
    default_type = 'p';
    $.getJSON($SCRIPT_ROOT + '/_get_new_place_title', {
        grade: String(default_grade),
        place: '1',
        type: 'p'
    }, function (data) {
        graph_title = String(data)
    });

    $.getJSON($SCRIPT_ROOT + '/_get_grade_place_total', {
        grade: String(default_grade),
        place: '1',
        type: 'p'
    }, function (data) {
        graphs = data;

        if(state){
        graph_data = [{
            x: graphs[0],
            y: graphs[1],
            type: 'bar'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
        }
        else{
        graph_data = [{
            labels: graphs[0],
            values: graphs[1],
            type: 'pie'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
    }
    });
});

$('#ensemble_tog').on('click', function() {
    default_type = 'e';
    $.getJSON($SCRIPT_ROOT + '/_get_new_place_title', {
        grade: String(default_grade),
        place: '1',
        type: 'e'
    }, function (data) {
        graph_title = String(data)
    });

    $.getJSON($SCRIPT_ROOT + '/_get_grade_place_total', {
        grade: String(default_grade),
        place: '1',
        type: 'e'
    }, function (data) {
        graphs = data;

        if(state){
        graph_data = [{
            x: graphs[0],
            y: graphs[1],
            type: 'bar'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
        }
        else{
        graph_data = [{
            labels: graphs[0],
            values: graphs[1],
            type: 'pie'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
    }
    });
});

$('#drumming_tog').on('click', function() {
    $.getJSON($SCRIPT_ROOT + '/_get_new_place_title', {
        grade: String(default_grade),
        place: '1',
        type: 'd'
    }, function (data) {
        graph_title = String(data)
    });

    $.getJSON($SCRIPT_ROOT + '/_get_grade_place_total', {
        grade: String(default_grade),
        place: '1',
        type: 'd'
    }, function (data) {
        graphs = data;

        if(state){
        graph_data = [{
            x: graphs[0],
            y: graphs[1],
            type: 'bar'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
        }
        else{
        graph_data = [{
            labels: graphs[0],
            values: graphs[1],
            type: 'pie'
        }];
        bar_layout['title'] = graph_title;
        pie_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
    }
    });
});

$('#piebar').on('click', function() {
    state = !state;
    if(state){
        $("#piebar").text('Pie Chart');
        graph_data = [{
            x: graphs[0],
            y: graphs[1],
            type: 'bar'
        }];
        Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
    }
    else{
        $("#piebar").text('Bar Chart');
        graph_data = [{
            labels: graphs[0],
            values: graphs[1],
            type: 'pie'
        }];
        Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
    }

});
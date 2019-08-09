var default_grade = '1';
var default_title = 'Grade One';
var default_type = 'Wins';
var graph_title;
var state = true;
var graphs;

var graph_data = [{
        x: "",
        y: "",
        type: 'bar'
    }];

var pie_layout = {
        title: default_title,
        autosize: true,
        showlegend: false,
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        },
    };

var bar_layout = {
        title: default_title,
        autosize: true,
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
        margin: {
            l: 50,
            r: 50,
            b: 250,
            t: 50,
            pad: 4
        },

    };

function create_totals_graph(new_graphs, graph_title) {
    graphs = new_graphs;
    default_title = graph_title;
    bar_layout['title'] = graph_title;
    graph_data[0]['x'] = new_graphs[0];
    graph_data[0]['y'] = new_graphs[1];
    Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud: true});
}

$('#ddselect button').on('click', function() {
    default_grade = $(this).text();
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
            type: String(default_type),
        }, function (data) {
            graph_title = String(data)
        });

        $.getJSON($SCRIPT_ROOT + '/_get_grade_place_total', {
            grade: String(default_grade),
            place: '1',
            type: default_type.charAt(0).toLowerCase()
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
});

$('#wins_tog').on('click', function() {
    default_type = 'w';
    $("#piping_tog, #drumming_tog, #ensemble_tog").removeClass("btn-success").addClass("btn-primary");
    $("#wins_tog").addClass("btn-success");
    $.getJSON($SCRIPT_ROOT + '/_get_new_title', {
        grade: String(default_grade),
        place: '1',
        type: 'Wins'
    }, function (data) {
        default_type = 'Wins';
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
            type: 'bar',
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
    $("#wins_tog, #drumming_tog, #ensemble_tog").removeClass("btn-success").addClass("btn-primary");
    $("#piping_tog").addClass("btn-success");
    $.getJSON($SCRIPT_ROOT + '/_get_new_place_title', {
        grade: String(default_grade),
        place: '1',
        type: 'Piping'
    }, function (data) {
        default_type = 'Piping';
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
    $("#piping_tog, #drumming_tog, #wins_tog").removeClass("btn-success").addClass("btn-primary");
    $("#ensemble_tog").addClass("btn-success");
    $.getJSON($SCRIPT_ROOT + '/_get_new_place_title', {
        grade: String(default_grade),
        place: '1',
        type: 'Ensemble'
    }, function (data) {
        default_type = 'Ensemble';
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
    $("#piping_tog, #wins_tog, #ensemble_tog").removeClass("btn-success").addClass("btn-primary");
    $("#drumming_tog").addClass("btn-success");
    $.getJSON($SCRIPT_ROOT + '/_get_new_place_title', {
        grade: String(default_grade),
        place: '1',
        type: 'Drumming'
    }, function (data) {
        default_type = 'Drumming';
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
            type: 'bar',
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
        $("#piebar").text('Pie Chart').removeClass("btn-info").addClass("btn-success");
        graph_data = [{
            x: graphs[0],
            y: graphs[1],
            type: 'bar'
        }];
        Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud:true});
    }
    else{
        $("#piebar").text('Bar Chart').removeClass("btn-success").addClass("btn-info");
        graph_data = [{
            labels: graphs[0],
            values: graphs[1],
            type: 'pie'
        }];
        Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud:true});
    }

});
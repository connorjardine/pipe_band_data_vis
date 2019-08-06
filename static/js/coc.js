var state = false;
var data = [];
var drumming_data = [];
var graph_title = "Overall Champion of Champions";
var d_graph_title = "Grade One Drumming Champion of Champions";

var layout = {
        title: String(graph_title),
        autosize: true
    };

function create_coc_graph(graphs, drumming_graphs) {
    for (let i = 0; i < Object.keys(graphs[0]).length; i++) {
        data.push({
            x: graphs[1],
            y: graphs[0][Object.keys(graphs[0])[i]][1],
            type: 'scatter',
            name: graphs[0][Object.keys(graphs[0])[i]][0]
        });
    }

    for (let i = 0; i < Object.keys(drumming_graphs[0]).length; i++) {
        drumming_data.push({
            x: drumming_graphs[1],
            y: drumming_graphs[0][Object.keys(drumming_graphs[0])[i]][1],
            type: 'scatter',
            name: drumming_graphs[0][Object.keys(drumming_graphs[0])[i]][0]
        });
    }
    Plotly.newPlot('myDiv', data, layout);
}

$('#ovdr').on('click', function() {
    state = !state;
    if(state){
        $("#ovdr").text(graph_title);
        layout['title'] = d_graph_title;
        Plotly.newPlot('myDiv', drumming_data, layout);
    }
    else{
        $("#ovdr").text(d_graph_title);
        layout['title'] = graph_title;
        Plotly.newPlot('myDiv', data, layout);
    }

});
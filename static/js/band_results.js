var current_grade = '1';
var current_band = '';
var compare_band = '';
var year_from = 2003;
var year_to = 2019;
var state = false;
var compare = false;
var shallow_data = [];

var controller = {'current_grade': '1', 'current_band': '', 'compare_band': '', 'year_from': 2003,
    'year_to': 2019, state: false, compare: false};

get_band_list('1');

var pie_layout = {
  autosize: true,
  title: '',
  annotations: [
    {
      font: {
        size: 11
      },
      showarrow: false,
      text: "Overall Placings",
    },
  ],
  height: 450,
  width: 450,
  showlegend: true,
  grid: {rows: 1, columns: 1}
};

var bar_layout = {
        autosize: true,
        xaxis: {
            tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
            }
        },
        yaxis: {
            title: 'Number of Placings',
            dtick: 5,
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
        height: 450,
        width: 500,
    };

var pie_graph_data = [{
  domain: {column: 0},
  hole: .4,
  type: 'pie'
}];

var doubled_pie_layout = {
  title: '',
  height: 450,
  width: 500,
  autosize: true,
  showlegend: false,
  grid: {rows: 1, columns: 2}
};

var doubled_pie_graph_data = [{
        domain: {
            row: 0,
            column: 0
          },
        hole: .4,
        type: 'pie'
    },
    {
        domain: {
            row: 0,
            column: 1
          },
        hole: .4,
        type: 'pie'
    }
    ];

var bar_graph_data = [{
    type: 'bar'
}];

var doubled_bar_layout = {
        barmode: 'group',
        autosize: true,
        xaxis: {
            tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
            }
        },
        yaxis: {
            title: 'Number of Placings',
            dtick: 5,
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
            x: 0.5,
            y: 1.0,
            bgcolor: 'rgba(255, 255, 255, 0)',
            bordercolor: 'rgba(255, 255, 255, 0)'
        },
        height: 500,
        width: 500,
    };

var doubled_bar_graph_data = [{
        x: "",
        y: "",
        type: 'bar'
    },
    {
        x: "",
        y: "",
        type: 'bar'
    }
    ];

function filterFunction() {
  var input, filter, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("band-select");
  a = div.getElementsByTagName("button");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function compfilterFunction() {
  var input, filter, a, i;
  input = document.getElementById("comp-myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("comp-band-select");
  a = div.getElementsByTagName("button");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function fromFilterFunction() {
  var input, filter, a, i;
  input = document.getElementById("from-input");
  filter = input.value.toUpperCase();
  div = document.getElementById("year-from-select");
  a = div.getElementsByTagName("button");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function toFilterFunction() {
  var input, filter, a, i;
  input = document.getElementById("to-input");
  filter = input.value.toUpperCase();
  div = document.getElementById("year-to-select");
  a = div.getElementsByTagName("button");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function updateSingleGraph(data, id, state){
    if (state) {
        pie_graph_data[0]['values'] = data['values'];
        pie_graph_data[0]['labels'] = data['labels'];
        pie_layout['title'] = data['title'];
        pie_layout['annotations'][0]['text'] = data['annotation'] + " Placings";
        Plotly.newPlot(id, pie_graph_data, pie_layout, {showSendToCloud: true, responsive: true});
    }
    else {
        bar_graph_data[0]['x'] = data['labels'];
        bar_graph_data[0]['y'] = data['values'];
        bar_layout['title'] = data['title'];
        Plotly.newPlot(id, bar_graph_data, bar_layout, {showSendToCloud: true, responsive: true});
    }
}

function updateDoubleGraph(data, id, state, current_band, compare_band, i) {
    if (state) {
        doubled_pie_graph_data[0]['values'] = data[0][i][1][1];
        doubled_pie_graph_data[0]['labels'] = data[0][i][1][0];
        doubled_pie_graph_data[1]['values'] = data[1][i][1][1];
        doubled_pie_graph_data[1]['labels'] = data[1][i][1][0];
        doubled_pie_graph_data[0]['name'] = current_band;
        doubled_pie_graph_data[1]['name'] = compare_band;
        doubled_pie_layout['title'] = data[0][i][0];
        Plotly.newPlot(id, doubled_pie_graph_data, doubled_pie_layout, {showSendToCloud: true, responsive: true});
    }
    else {
        doubled_bar_graph_data[0]['x'] = data[0][i][1][0];
        doubled_bar_graph_data[0]['y'] = data[0][i][1][1];
        doubled_bar_graph_data[1]['x'] = data[1][i][1][0];
        doubled_bar_graph_data[1]['y'] = data[1][i][1][1];
        doubled_bar_graph_data[0]['name'] = current_band;
        doubled_bar_graph_data[1]['name'] = compare_band;
        doubled_bar_layout['title'] = data[0][i][0];
        Plotly.newPlot(id, doubled_bar_graph_data, doubled_bar_layout, {showSendToCloud: true, responsive: true});
    }
}

function update_band_graph(grade, band, comp_band, compare, state) {
    $.getJSON($SCRIPT_ROOT + '/_update_band_data', {
        grade: String(grade),
        band: String(band),
        comp_band: String(comp_band),
        year_from: year_from,
        year_to: year_to,
    }, function (data) {
        shallow_data = data;
        shallow_update_band_graph(grade, band, comp_band, data, compare, state);
        $.LoadingOverlay("hide");
        $('#band-name').text(String(controller['current_band']));
        $("#chart-col").show();
    });
}

function shallow_update_band_graph(grade, band, comp_band, data, compare, state) {
    for (var i = 0; i < data[0].length; i++) {
        var id = 'myDiv' + String(i);
        if (!compare) {
            var copy_values = data[0][i][1][1].slice();
            var copy_labels = data[0][i][1][0].slice();
            var k = copy_labels.length;
            while(k--){
                if (copy_values[k] === 0){
                    copy_values.splice(k, 1);
                    copy_labels.splice(k, 1);
                }
            }
            var send_data = {'annotation': data[0][i][2], 'title': data[0][i][0], 'labels': copy_labels, 'values': copy_values};
            updateSingleGraph(send_data, id, state, i)
        }
        else {
            updateDoubleGraph(data, id, state, controller['current_band'], controller['compare_band'], i)
        }
    }
}

function get_band_list(grade) {
    $.getJSON($SCRIPT_ROOT + '/_get_band_list', {
        grade: String(grade),
        year_from: year_from,
        year_to: year_to
    }, function (data) {
        $('#band-select').html("").append("<input type=\"text\" placeholder=\"Search..\" id=\"myInput\" onkeyup=\"filterFunction()\">");
        for (var i = 0; i < data.length; i++) {
            $('#band-select').append("<button value=\"1\" id=\"sel-button\" class=\"dropdown-item\" type=\"button\">" + data[i] + "</button>");
        }
        $('#comp-band-select').html("").append("<input type=\"text\" placeholder=\"Search..\" id=\"comp-myInput\" onkeyup=\"compfilterFunction()\">");
        for (var i = 0; i < data.length; i++) {
            $('#comp-band-select').append("<button value=\"1\" id=\"sel-button\" class=\"dropdown-item\" type=\"button\">" + data[i] + "</button>");
        }
    });
}


$('#dropdown-band').text("Band");
$('#comp-dropdown-band').text("Comparison Band");


$('#ddselect button').on('click', function() {
    if (controller['current_grade'] !== $(this).text()) {
        controller['current_grade'] = $(this).text();
        get_band_list($(this).text());
        $('#dropdownMenu2').text("Chosen Grade:   "+String(controller['current_grade']));
        $('#comp-dropdown-band').text("Choose a Band to Compare");
        $('#dropdown-band').text("Choose a Band");
        $('#band-name').text("");
        $("#chart-col").hide();


    }
});

$('#band-select').on('click', '#sel-button', function() {
    controller['current_band'] = $(this).text();
    $('#band-results-submit').removeAttr("disabled");
    $('#dropdown-band').text("Chosen Band:   " + String(controller['current_band']));
});

$('#comp-band-select').on('click', '#sel-button', function() {
    controller['compare_band'] = $(this).text();
    $('#comp-dropdown-band').text("Comparison Band:   " + String(controller['compare_band']));

});

$('#piebar').on('click', function() {
    controller['state'] = !controller['state'];
    if(!controller['state']){
        $("#piebar").text('Pie Chart').removeClass("btn-info").addClass("btn-primary");
        shallow_update_band_graph(controller['current_grade'], controller['current_band'],
            controller['compare_band'], shallow_data, controller['compare'], controller['state']);
    }
    else{
        $("#piebar").text('Bar Chart').removeClass("btn-primary").addClass("btn-info");
        shallow_update_band_graph(controller['current_grade'], controller['current_band'],
            controller['compare_band'], shallow_data, controller['compare'], controller['state']);
    }

});

$('#compare').on('click', function() {
    controller['compare'] = !controller['compare'];
    console.log(controller);
    if(controller['compare']){
        $("#compare").text('No Comparison').removeClass("btn-info").addClass("btn-primary");
        shallow_update_band_graph(controller['current_grade'], controller['current_band'],
            controller['compare_band'], shallow_data, controller['compare'], controller['state']);
        $('#band-name').text(String(controller['current_band']) + " - " + String(controller['compare_band']));
    }
    else{
        $("#compare").text('Comparison').removeClass("btn-primary").addClass("btn-info");
        shallow_update_band_graph(controller['current_grade'], controller['current_band'],
            controller['compare_band'], shallow_data, controller['compare'], controller['state']);
        $('#band-name').text(String(controller['current_band']));
    }

});

$('#year-from-select button').on('click', function() {
    controller['year_from'] = $(this).text();
});

$('#year-to-select button').on('click', function() {
    controller['year_to'] = $(this).text();
});

$('#band-results-submit').on('click', function() {
    if (controller['current_band'] !== controller['compare_band'] && controller['current_band'] !== "") {
        $.LoadingOverlay("show", {
            image       : "",
            text        : "Waiting for the pipers..."
        });
        setTimeout(function(){
            $.LoadingOverlay("text", "Yep, still tuning...");
        }, 2500);
        update_band_graph(controller['current_grade'], controller['current_band'], controller['compare_band']);
    }
    else {
        console.log("show error for this.")
    }
});


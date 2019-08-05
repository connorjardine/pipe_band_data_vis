var current_grade = '1';
var current_band = 'Field Marshal Montgomery';
var compare_band = 'Inveraray and District';
var state = true;
var compare = false;
var shallow_data = [];

get_band_list('1');

var pie_layout = {
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
  width: 500,
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
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        },

    };

var pie_graph_data = [{
  domain: {column: 0},
  name: current_band,
  hole: .4,
  type: 'pie'
}];

var doubled_pie_layout = {
  title: '',
  height: 450,
  width: 500,
  autosize: true,
  showlegend: true,
  grid: {rows: 1, columns: 2}
};

var doubled_pie_graph_data = [{
        domain: {
            row: 0,
            column: 0
          },
        name: current_band,
        hole: .4,
        type: 'pie'
    },
    {
        domain: {
            row: 0,
            column: 1
          },
        name: compare_band,
        hole: .4,
        type: 'pie'
    }
    ];

var bar_graph_data = [{
    x: "",
    y: "",
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
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50,
            pad: 4
        },

    };

var doubled_bar_graph_data = [{
        name: current_band,
        x: "",
        y: "",
        type: 'bar'
    },
    {
        name: compare_band,
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

function update_band_graph(grade, band, comp_band, compare) {
    if (!compare){
        comp_band = 'none';
    }
    $.getJSON($SCRIPT_ROOT + '/_update_band_data', {
        grade: String(grade),
        band: String(band),
        comp_band: String(comp_band)
    }, function (data) {
        shallow_data = data;
        for(var i = 0; i < data[0].length; i++) {
            var id = 'myDiv' + String(i);
            if (!compare) {
                $('#band-name').text(String(band));
                if (state) {
                    pie_graph_data[0]['values'] = data[0][i][1][1];
                    pie_graph_data[0]['labels'] = data[0][i][1][0];
                    pie_layout['title'] = data[0][i][0];
                    pie_layout['annotations'][0]['text'] = data[0][i][2] + " Placings";
                    Plotly.newPlot(id, pie_graph_data, pie_layout, {showSendToCloud: true, responsive: true});
                }
                else {
                    bar_graph_data[0]['x'] = data[0][i][1][0];
                    bar_graph_data[0]['y'] = data[0][i][1][1];
                    bar_layout['title'] = data[0][i][0];
                    Plotly.newPlot(id, bar_graph_data, bar_layout, {showSendToCloud: true, responsive: true});
                }

            }
            else {
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
            $.LoadingOverlay("hide");
            $('#dropdown-band').text("Chosen Band:   " + String(current_band));
            $("#chart-col").show();
            if (compare) {
                $('#comp-dropdown-band').text("Comparison Band:   " + String(compare_band));
                $('#band-name').text(String(current_band) + " - " + String(compare_band));
            }
        }
    });
}

function shallow_update_band_graph(grade, band, comp_band, data) {
    if ((data[1] === undefined || data[1].length === 0) && compare === true) {
        $.LoadingOverlay("show");
        update_band_graph(grade, band, comp_band, compare)
    }
    else {
        for (var i = 0; i < data[0].length; i++) {
            var id = 'myDiv' + String(i);
            if (!compare) {
                $('#band-name').text(String(band));
                if (state) {
                    pie_graph_data[0]['values'] = data[0][i][1][1];
                    pie_graph_data[0]['labels'] = data[0][i][1][0];
                    pie_layout['title'] = data[0][i][0];
                    pie_layout['annotations'][0]['text'] = data[0][i][2] + " Placings";
                    Plotly.newPlot(id, pie_graph_data, pie_layout, {showSendToCloud: true, responsive: true});
                }
                else {
                    bar_graph_data[0]['x'] = data[0][i][1][0];
                    bar_graph_data[0]['y'] = data[0][i][1][1];
                    bar_layout['title'] = data[0][i][0];
                    Plotly.newPlot(id, bar_graph_data, bar_layout, {showSendToCloud: true, responsive: true});
                }

            }
            else {
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
        }
    }
}

function get_band_list(grade) {
    $.getJSON($SCRIPT_ROOT + '/_get_band_list', {
        grade: String(grade)
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

$.LoadingOverlay("show");
update_band_graph(current_grade, current_band, compare_band);
$('#dropdown-band').text("Chosen Band:   " + String(current_band));
$('#comp-dropdown-band').text("Comparison Band:   " + String(compare_band));


$('#ddselect button').on('click', function() {
    if (current_grade !== $(this).text()) {
        current_grade = $(this).text();
        get_band_list(current_grade);
        $('#dropdownMenu2').text("Chosen Grade:   "+String(current_grade));
        $('#comp-dropdown-band').text("Choose a Band to Compare");
        $('#dropdown-band').text("Choose a Band");
        $('#band-name').text("");
        $("#chart-col").hide();


    }
});

$('#band-select').on('click', '#sel-button', function() {
    if (current_grade !== $(this).text()) {
        current_band = $(this).text();
        $.LoadingOverlay("show");
        update_band_graph(current_grade, current_band, compare_band);

    }
});

$('#comp-band-select').on('click', '#sel-button', function() {
    compare_band = $(this).text();
    console.log(compare, compare_band, current_band);
    if (current_band !== compare_band && compare) {
        $.LoadingOverlay("show");
        console.log(compare_band);
        update_band_graph(current_grade, current_band, compare_band);
    }
    else{
        $('#comp-dropdown-band').text("Comparison Band:   " + String(compare_band));
    }
});

$('#piebar').on('click', function() {
    state = !state;
    if(!state){
        $("#piebar").text('Pie Chart').removeClass("btn-info").addClass("btn-primary");
        shallow_update_band_graph(current_grade, current_band, compare_band, shallow_data);
    }
    else{
        $("#piebar").text('Bar Chart').removeClass("btn-primary").addClass("btn-info");
        shallow_update_band_graph(current_grade, current_band, compare_band, shallow_data);
    }

});

$('#compare').on('click', function() {
    compare = !compare;
    if(compare){
        $("#compare").text('No Comparison').removeClass("btn-info").addClass("btn-primary");
        shallow_update_band_graph(current_grade, current_band, compare_band, shallow_data);
    }
    else{
        $("#compare").text('Comparison').removeClass("btn-primary").addClass("btn-info");
        shallow_update_band_graph(current_grade, current_band, compare_band, shallow_data);
    }

});


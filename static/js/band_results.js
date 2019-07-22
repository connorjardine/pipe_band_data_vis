var current_grade = '1';
var current_band = 'Field Marshal Montgomery';
var compare_band = 'Inveraray and District';
var state = true;
var compare = false;

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
  width: 450,
  showlegend: false,
  grid: {rows: 1, columns: 1}
};

var bar_layout = {

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
        height: 450,
        width: 450,
        margin: {
            l: 50,
            r: 50,
            b: 250,
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

var bar_graph_data = [{
    x: "",
    y: "",
    type: 'bar'
}];

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

function update_band_graph(grade, band, comp_band) {
    $.getJSON($SCRIPT_ROOT + '/_update_band_data', {
        grade: String(grade),
        band: String(band)
    }, function (data) {
        $('#band-name').text(String(band));
        for(var i = 0; i < data.length; i++) {
            console.log(data[i]);
            var id = 'myDiv' + String(i);
            console.log(id);
            if (!compare) {
                if (state) {
                    console.log(data[i][1][1], data[i][1][0]);
                    pie_graph_data[0]['values'] = data[i][1][1];
                    pie_graph_data[0]['labels'] = data[i][1][0];
                    pie_layout['title'] = data[i][0];
                    console.log(pie_graph_data);
                    Plotly.newPlot(id, pie_graph_data, pie_layout, {showSendToCloud: true});
                }
                else {
                    bar_graph_data[0]['x'] = data[i][1][0];
                    bar_graph_data[0]['y'] = data[i][1][1];
                    bar_layout['title'] = data[i][0];
                    Plotly.newPlot(id, bar_graph_data, bar_layout, {showSendToCloud: true});
                }

            }
        }
    });
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

update_band_graph(current_grade, current_band, compare_band);

$('#ddselect button').on('click', function() {
    if (current_grade !== $(this).text()) {
        current_grade = $(this).text();
        get_band_list(current_grade);
        $('#dropdownMenu2').text("Chosen Grade:   "+String(current_grade));
    }
});

$('#band-select').on('click', '#sel-button', function() {
    if (current_grade !== $(this).text()) {
        current_band = $(this).text();
        $('#dropdown-band').text("Chosen Band:   "+String(current_band));
        $('#band-name').text(String(current_band));
        update_band_graph(current_grade, current_band, compare_band);
    }
});

$('#comp-band-select').on('click', '#sel-button', function() {
    compare_band = $(this).text();
    if (current_grade !== $(this).text() && current_band !== compare_band) {
        $('#comp-dropdown-band').text("Comparison Band:   "+String(compare_band));
        $('#band-name').text(String(current_band));
        update_band_graph(current_grade, current_band, compare_band);
    }
});

$('#piebar').on('click', function() {
    state = !state;
    if(!state){
        $("#piebar").text('Pie Chart').removeClass("btn-info").addClass("btn-primary");
        update_band_graph(current_grade, current_band, compare_band);
    }
    else{
        $("#piebar").text('Bar Chart').removeClass("btn-primary").addClass("btn-info");
        update_band_graph(current_grade, current_band, compare_band);
    }

});

$('#compare').on('click', function() {
    compare = !compare;
    if(compare){
        $("#compare").text('No Comparison').removeClass("btn-info").addClass("btn-primary");
        update_band_graph(current_grade, current_band, compare_band);
    }
    else{
        $("#compare").text('Comparison').removeClass("btn-primary").addClass("btn-info");
        update_band_graph(current_grade, current_band, compare_band);
    }

});


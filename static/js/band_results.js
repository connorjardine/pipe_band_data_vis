var current_grade = '1';
var current_band = 'Field Marshal Montgomery';
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

var graph_data = [{
  domain: {column: 0},
  name: current_band,
  hole: .4,
  type: 'pie'
}];


function update_band_graph(grade, band) {
    $.getJSON($SCRIPT_ROOT + '/_update_band_data', {
        grade: String(grade),
        band: String(band)
    }, function (data) {
        console.log(data);
        pie_layout['title'] = data[0];
        graph_data[0]['values'] = data[1][1];
        graph_data[0]['labels'] = data[1][0];
        console.log(pie_layout);
        console.log(graph_data);

        Plotly.newPlot('myDiv', graph_data, pie_layout, {showSendToCloud: true});
        Plotly.newPlot('myDiv1', graph_data, pie_layout, {showSendToCloud: true});
        Plotly.newPlot('myDiv2', graph_data, pie_layout, {showSendToCloud: true});
        Plotly.newPlot('myDiv3', graph_data, pie_layout, {showSendToCloud: true});
    });
}

function get_band_list(grade) {
    $.getJSON($SCRIPT_ROOT + '/_get_band_list', {
        grade: String(grade)
    }, function (data) {
        $('#band-select').html("");
        $('#band-select').append("<input type=\"text\" placeholder=\"Search..\" id=\"myInput\" onkeyup=\"filterFunction()\">");
        for (var i = 0; i < data.length; i++) {
            $('#band-select').append("<button value=\"1\" id=\"sel-button\" class=\"dropdown-item\" type=\"button\">" + data[i] + "</button>");
        }
    });
}

update_band_graph(current_grade, current_band);

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
        update_band_graph(current_grade, current_band);
    }
});

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
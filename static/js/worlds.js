var default_title = 'Grade One';
var default_grade = '1';
var default_year_from = 2003;
var default_year_to = 2018;
var curr_grade;
var curr_year_from;
var worlds_table;
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
    autosize: true,
    xaxis: {
        tickfont: {
            size: 14,
            color: 'rgb(107, 107, 107)'
        }
    },
    yaxis: {
        title: 'Number of Wins',
        dtick: 1,
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

function checkValidYear(year_from, year_to) {
    if (year_from > year_to) {
        $("#pbAlert").show();
        setTimeout(function(){
            $("#pbAlert").hide();
        }, 3000);
        return false;
    }
    return true;
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

function create_worlds_graph(new_graphs, graph_title) {
    graphs = new_graphs;
    default_title = graph_title;
    bar_layout['title'] = graph_title;
    graph_data[0]['x'] = new_graphs[0];
    graph_data[0]['y'] = new_graphs[1];
    Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud: true});
}

function update_table() {
    curr_grade = default_grade;
    $.getJSON($SCRIPT_ROOT + '/_get_worlds_totals', {
        grade: String(default_grade),
        place: '1',
        year_from: default_year_from,
        year_to: default_year_to
    }, function (data) {
        worlds_table = data['table_data'];
        graph_title = String(worlds_table[0]);
        $('#worlds_table').removeClass("table-striped table-bordered table-hover");
        if (default_grade !== '1') {
            $('#worlds_table').html("").append("<thead class=\"thead-dark\">\n" +
                "                        <tr>\n" +
                "                            <th scope=\"col\">Year</th>\n" +
                "                            <th scope=\"col\">Grade</th>\n" +
                "                            <th scope=\"col\">Competition</th>\n" +
                "                            <th scope=\"col\">Winning Band</th>\n" +
                "                            <th scope=\"col\">Overall Total</th>\n" +
                "                        </tr>\n" +
                "                    </thead>")
            for (var i = 0; i < worlds_table[1].length; i++) {
                var row = worlds_table[1][i];
                var row_td = "";
                for (var k = 0; k < row.length; k++) {
                    row_td += "<td>" + row[k] + "</td>"
                }
                $('#worlds_table').append("<tr>" + row_td + "</tr>");
            }
        }
        else {
            $('#worlds_table').html("").append("<thead class=\"thead-dark\">\n" +
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
            for (var i = 0; i < worlds_table[1].length; i++) {
                var row = worlds_table[1][i];
                var row_td = "";
                for (var k = 0; k < row.length; k++) {
                    row_td += "<td>" + row[k] + "</td>"
                }
                $('#worlds_table').append("<tr>" + row_td + "</tr>");
            }
        }
        $('#worlds_table').addClass("table-striped table-bordered table-hover");

        graphs = data['graph'];
        graph_data = [{
            x: graphs[0],
            y: graphs[1],
            type: 'bar'
        }];
        bar_layout['title'] = graph_title;
        Plotly.newPlot('myDiv', graph_data, bar_layout, {showSendToCloud: true});
    });
}



$('#worlds-submit').on('click', function() {
    update_table()
});

$('#year-from-select button').on('click', function() {
    if (checkValidYear($(this).text(), default_year_to)) {
        default_year_from = $(this).text();
        $('#y-from').text("Year From: " + default_year_from);
    }
});

$('#year-to-select button').on('click', function() {
    if (checkValidYear(default_year_from, $(this).text())) {
        default_year_to = $(this).text();
        $('#y-to').text("Year To: " + default_year_to);
    }
});

$('#ddselect button').on('click', function() {
    default_grade = $(this).text();
    $('#dropdownMenu2').text("Grade: " + default_grade);
});
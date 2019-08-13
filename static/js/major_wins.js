var default_grade = '1';
var default_type = 'w';
var year_from = 2003;
var year_to = 2018;
var graph_title;
var state = true;
var graphs;

var pie_layout = {
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
    autosize: true,
    xaxis: {
        tickfont: {
            size: 14,
            color: 'rgb(107, 107, 107)'
        }
    },
    yaxis: {
        title: 'Number of Wins',
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


function updateGrade(grade, place, type, year_from, year_to) {
    console.log(grade, place, type, year_from, year_to);
    $.getJSON($SCRIPT_ROOT + '/_get_grade_total', {
        grade: String(grade),
        place: place,
        type: type,
        year_from: year_from,
        year_to: year_to,
    }, function (data) {
        graphs = data['data'];
        graph_title = String(data['title']);
        console.log(data);
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

updateGrade('1', '1', 'w', 2003, 2018);

function updateSelectedButtonStyle(selector_to, other_selectors) {
    $(other_selectors).removeClass("btn-success").addClass("btn-primary");
    $(selector_to).addClass("btn-success");
}

function updatePieBar(state) {
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

$('#ddselect button').on('click', function() {
    default_grade = $(this).text();
    updateGrade(default_grade, '1', default_type, year_from, year_to)
});

$('#wins_tog').on('click', function() {
    default_type = 'w';
    updateSelectedButtonStyle("#wins_tog", "#piping_tog, #drumming_tog, #ensemble_tog");
    updateGrade(default_grade, '1', default_type, year_from, year_to)
});

$('#piping_tog').on('click', function() {
    default_type = 'p';
    updateSelectedButtonStyle("#piping_tog", "#wins_tog, #drumming_tog, #ensemble_tog");
    updateGrade(default_grade, '1', default_type, year_from, year_to)
});

$('#ensemble_tog').on('click', function() {
    default_type = 'e';
    updateSelectedButtonStyle("#ensemble_tog", "#piping_tog, #drumming_tog, #wins_tog");
    updateGrade(default_grade, '1', default_type, year_from, year_to)
});

$('#drumming_tog').on('click', function() {
    default_type = 'd';
    updateSelectedButtonStyle("#drumming_tog", "#piping_tog, #wins_tog, #ensemble_tog");
    updateGrade(default_grade, '1', default_type, year_from, year_to)
});

$('#piebar').on('click', function() {
    state = !state;
    updatePieBar(state)
});

$('#year-from-select button').on('click', function() {
    if (checkValidYear($(this).text(), year_to)) {
        year_from = $(this).text();
        $('#y-from').text("Year From: " + year_from);
        updateGrade(default_grade, '1', default_type, year_from, year_to)
    }
});

$('#year-to-select button').on('click', function() {
    if (checkValidYear(year_from, $(this).text())) {
        year_to = $(this).text();
        $('#y-to').text("Year To: " + year_to);
        updateGrade(default_grade, '1', default_type, year_from, year_to)
    }
});
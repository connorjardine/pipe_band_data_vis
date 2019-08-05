from flask import Flask, render_template, request, jsonify
import json
import plotly

from modules.generate_data.band_results import *
from modules.generate_data.other_results import *
from modules.generate_data.worlds import *
from modules.db.db import *

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html',
                           data=jsonpickle.decode(pull_data(helper_collection, {"type": "slams"})[0]['data']))


@app.route('/major_totals')
def grade():
    names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_overall"})[0]['data']))
    graphJSON = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('major_totals.html',
                           graphJSON=graphJSON, graph_title="Total Grade One Majors Won")


@app.route('/worlds')
def worlds():
    data = get_grade1_worlds_totals('1')
    names, values = zip(*data[0])
    graphJSON = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('worlds.html',
                           graphJSON=graphJSON, graph_title="Total Number of Worlds Wins in Grade One (2003-2018)", worlds_list=data[1])


@app.route('/band_results')
def band_results():
    return render_template('band_results.html', data="data")


@app.route('/champion_of_champions')
def prog_coc():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    data = pull_data(helper_collection,{"type": "g1_coc"})
    drumming_data = pull_data(helper_collection, {"type": "g1_drumming_coc"})
    drumming_graphJSON = json.dumps([jsonpickle.decode(drumming_data[0]['data']), y_list], cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON = json.dumps([jsonpickle.decode(data[0]['data']), y_list], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('champion_of_champions.html',
                           graphJSON=graphJSON, d_graph_json=drumming_graphJSON,
                           graph_title="Grade One Overall Champion of Champions")


@app.route('/_get_grade_total')
def get_grade_total():
    upd_grade = request.args.get('grade', '1', type=str)
    place = request.args.get('place', '1', type=str)
    if upd_grade == '1':
        names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_overall"})[0]['data']))
    else:
        upd_grade = convert_grade(upd_grade)
        names, values = zip(*return_other_data(place, upd_grade))
    graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json


@app.route('/_get_new_title')
def get_new_title():
    grade = request.args.get('grade', '1', type=str)
    graph_title = ("Total Number of Overall Wins in Grade " + grade + " (2003-2018)")
    return graph_title


@app.route('/_get_grade_place_total')
def get_grade_place_total():
    upd_grade = request.args.get('grade', '1', type=str)
    place = request.args.get('place', '1', type=str)
    type = request.args.get('type', 'd', type=str)
    if upd_grade == '1':
        if type == 'd':
            names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_drumming"})[0]['data']))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
        if type == 'e':
            names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_ensemble"})[0]['data']))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
        else:
            names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_piping"})[0]['data']))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
    else:
        if upd_grade == 'Juv':
            names, values = zip(*return_other_placings_data(place, 'juv', type))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
        if upd_grade == 'Nov A':
            names, values = zip(*return_other_placings_data(place, 'Nov%20A', type))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
        if upd_grade == 'Nov B':
            names, values = zip(*return_other_placings_data(place, 'Nov%20B', type))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
        else:
            names, values = zip(*return_other_placings_data(place, upd_grade, type))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json


@app.route('/_get_new_place_title')
def get_new_place_title():
    grade = request.args.get('grade', '1', type=str)
    new_type = request.args.get('type', '1', type=str)
    graph_title = jsonify("Total Number of " + new_type + " Wins in Grade " + grade + " (2003-2018)")
    return graph_title


@app.route('/_get_worlds_total')
def get_worlds_total():
    grade = request.args.get('grade', '1', type=str)
    place = request.args.get('place', '1', type=str)
    if grade == '1':
        names, values = zip(*get_grade1_worlds_totals('1')[0])
        graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
    else:
        names, values = zip(*return_other_worlds_data('1', grade, 'World Championships')[0])
        graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json


@app.route('/_get_worlds_data')
def get_worlds_data():
    grade = request.args.get('grade', '1', type=str)
    graph_title = "Total Number of Worlds Wins in Grade " + grade + " (2003-2018)"
    if grade == '1':
        return jsonify([graph_title, get_grade1_worlds_totals('1')[1]])
    return jsonify([graph_title, return_other_worlds_data('1', grade, 'World Championships')[1]])


@app.route('/_update_band_data')
def update_band_data():
    grade = request.args.get('grade', '1', type=str)
    band = request.args.get('band', '1', type=str)
    compare_band = request.args.get('comp_band', 'none', type=str)
    data = [[], []]
    print(grade, band, compare_band)
    if grade == '1':
        band_data = get_bands_data(grade, band)
        for k in band_data:
            graph_title = str(k[2]) + " Totals in Grade " + grade + " (2003-2018)"
            names, values = zip(*conv_key_to_str(k[1]).items())
            data[0].append([graph_title, [names, values], str(k[2])])

        if compare_band != 'none':
            compare_band_data = get_bands_data(grade, compare_band)
            for k in compare_band_data:
                graph_title = str(k[2]) + " Totals in Grade " + grade + " (2003-2018)"
                names, values = zip(*conv_key_to_str(k[1]).items())
                data[1].append([graph_title, [names, values], str(k[2])])
    else:
        band_data = get_bands_data(grade, band)
        for k in band_data:
            graph_title = str(k[2]) + " Totals in Grade " + grade + " (2003-2018)"
            names, values = zip(*conv_key_to_str(k[1]).items())
            data[0].append([graph_title, [names, values], str(k[2])])
        if compare_band != 'none':
            compare_band_data = return_other_band_data(grade, compare_band)
            for k in compare_band_data:
                graph_title = str(k[2]) + " Totals in Grade " + grade + " (2003-2018)"
                names, values = zip(*conv_key_to_str(k[1]).items())
                data[1].append([graph_title, [names, values], str(k[2])])
    return jsonify(data)


@app.route('/_get_band_list')
def get_band_list():
    grade = request.args.get('grade', '1', type=str)
    return jsonify(get_bands_list(grade))


if __name__ == "__main__":
    app.run(host="0.0.0.0")




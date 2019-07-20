from flask import Flask, render_template, request, jsonify
import json
import plotly

from modules.grade1_results import *
from modules.other_results import *
from modules.progressive_coc import *
from modules.worlds import *

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
helper_collection = db.band_helper_data

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/major_totals')
def grade():
    names, values = zip(*jsonpickle.decode(helper_collection.find({"type": "g1_overall"})[0]['data']))
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


@app.route('/champion_of_champions')
def prog_coc():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    data = helper_collection.find({"type": "g1_coc"})
    drumming_data = helper_collection.find({"type": "g1_drumming_coc"})
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
        names, values = zip(*jsonpickle.decode(helper_collection.find({"type": "g1_overall"})[0]['data']))
    else:
        if upd_grade == 'Juv':
            upd_grade = 'juv'
        if upd_grade == 'Nov A':
            upd_grade = 'Nov%20A'
        if upd_grade == 'Nov B':
            upd_grade = 'Nov%20B'
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
    print(type)
    if upd_grade == '1':
        if type == 'd':
            names, values = zip(*jsonpickle.decode(helper_collection.find({"type": "g1_drumming"})[0]['data']))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
        if type == 'e':
            names, values = zip(*jsonpickle.decode(helper_collection.find({"type": "g1_ensemble"})[0]['data']))
            graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
            return graph_json
        else:
            names, values = zip(*jsonpickle.decode(helper_collection.find({"type": "g1_piping"})[0]['data']))
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


if __name__ == "__main__":
    app.run()
    #app.run(host="0.0.0.0", port=80)




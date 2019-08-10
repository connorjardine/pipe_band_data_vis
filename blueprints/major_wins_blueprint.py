from flask import Blueprint, render_template, request, jsonify
import json
import jsonpickle
import plotly

from modules.db.db import *
from modules.generate_data.band_results import convert_grade
from modules.generate_data.other_results import return_other_data, return_other_placings_data

major_wins = Blueprint('major_wins', __name__)


@major_wins.route('/major_totals')
def get_major_wins():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_overall"})[0]['data']))
    graphJSON = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('major_totals.html',
                           graphJSON=graphJSON, graph_title="Total Grade One Majors Won", year_list=y_list)


@major_wins.route('/_get_grade_total')
def get_grade_total():
    upd_grade = request.args.get('grade', '1', type=str)
    place = request.args.get('place', '1', type=str)
    year_from = request.args.get('year_from', 2003, type=int)
    year_to = request.args.get('year_to', 2018, type=int)
    if upd_grade == '1':
        names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_overall"})[0]['data']))
    else:
        upd_grade = convert_grade(upd_grade)
        names, values = zip(*return_other_data(place, upd_grade))
    graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json


@major_wins.route('/_get_new_title')
def get_new_title():
    grade = request.args.get('grade', '1', type=str)
    graph_title = ("Total Number of Overall Wins in Grade " + grade + " (2003-2018)")
    return graph_title


@major_wins.route('/_get_grade_place_total')
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


@major_wins.route('/_get_new_place_title')
def get_new_place_title():
    grade = request.args.get('grade', '1', type=str)
    new_type = request.args.get('type', '1', type=str)
    graph_title = jsonify("Total Number of " + new_type + " Wins in Grade " + grade + " (2003-2018)")
    return graph_title
import plotly
import json
from flask import Blueprint, render_template, request, jsonify

from modules.generate_data.worlds import get_grade1_worlds_totals, return_other_worlds_data

worlds = Blueprint('worlds', __name__)


@worlds.route('/worlds')
def get_worlds():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    data = get_grade1_worlds_totals('1', 2003, 2018)
    names, values = zip(*data[0])
    graphJSON = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('worlds.html',
                           graphJSON=graphJSON,
                           graph_title="Total Number of Worlds Wins in Grade {0} ({1}-{2})".format('1', 2003, 2018),
                           worlds_list=data[1], year_list=y_list)


@worlds.route('/_get_worlds_data')
def get_worlds_data():
    grade = request.args.get('grade', '1', type=str)
    year_from = request.args.get('year_from', 2003, type=int)
    year_to = request.args.get('year_to', 2018, type=int)
    graph_title = "Total Number of Worlds Wins in Grade {0} ({1}-{2})".format(str(grade), str(year_from), str(year_to))
    if grade == '1':
        return jsonify([graph_title, get_grade1_worlds_totals('1', year_from, year_to)[1]])
    return jsonify([graph_title, return_other_worlds_data('1', grade, year_from, year_to, 'World Championships')[1]])


@worlds.route('/_get_worlds_total')
def get_worlds_total():
    grade = request.args.get('grade', '1', type=str)
    year_from = request.args.get('year_from', 2003, type=int)
    year_to = request.args.get('year_to', 2018, type=int)
    if grade == '1':
        names, values = zip(*get_grade1_worlds_totals('1', year_from, year_to)[0])
        graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
    else:
        names, values = zip(*return_other_worlds_data('1', grade, year_from, year_to, 'World Championships')[0])
        graph_json = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
        return graph_json
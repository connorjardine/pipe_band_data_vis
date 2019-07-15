from flask import Flask, render_template, request, jsonify
import json
import plotly

from grade1_results import *
from other_results import *
from progressive_coc import *

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
helper_collection = db.band_helper_data

app = Flask(__name__)


@app.route('/major_totals')
def grade():

    names, values = zip(*return_g1_data('1'))
    graphJSON = json.dumps([names, values], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('major_totals.html',
                           graphJSON=graphJSON, graph_title="Total Grade One Majors Won")




@app.route('/champion_of_champions')
def prog_coc():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    data = helper_collection.find({"type": "g1_coc"})
    drumming_data = helper_collection.find({"type": "g1_drumming_coc"})
    drumming_graphJSON = json.dumps([jsonpickle.decode(drumming_data[0]['data']), y_list], cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON = json.dumps([jsonpickle.decode(data[0]['data']), y_list], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('champion_of_champions.html',
                           graphJSON=graphJSON, d_graph_json=drumming_graphJSON,
                           d_graph_title="Grade One Drumming Champion of Champions",
                           graph_title="Grade One Overall Champion of Champions")


@app.route('/_get_grade_total')
def get_grade_total():
    upd_grade = request.args.get('grade', '1', type=str)
    place = request.args.get('place', '1', type=str)
    if upd_grade == '1':
        names, values = zip(*return_g1_data(place))
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
    graph_title = jsonify("Total Grade " + grade + " Majors Won")
    return graph_title




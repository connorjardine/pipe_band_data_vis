from flask import Blueprint, render_template
import json
import jsonpickle
import plotly

from modules.generate_data.perfect_scores import get_perfect_scores
from modules.db.db import *

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
def get_dashboard():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    #ps_data=jsonpickle.decode(pull_data(helper_collection, {"type": "perfect_scores"})[0]['data'])
    data = pull_data(helper_collection, {"type": "g1_coc"})
    drumming_data = pull_data(helper_collection, {"type": "g1_drumming_coc"})
    drumming_graphJSON = json.dumps([jsonpickle.decode(drumming_data[0]['data']), y_list],
                                    cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON = json.dumps([jsonpickle.decode(data[0]['data']), y_list], cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html',
                           gs_data=jsonpickle.decode(pull_data(helper_collection, {"type": "slams"})[0]['data']),
                           ps_data=get_perfect_scores(),
                           graphJSON=graphJSON, d_graph_json=drumming_graphJSON,
                           graph_title="Grade One Overall Champion of Champions")
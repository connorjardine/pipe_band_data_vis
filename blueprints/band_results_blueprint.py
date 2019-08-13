from flask import Blueprint, render_template, request, jsonify

from modules.generate_data.band_results.band_results import get_bands_list, update_band_data

band_results = Blueprint('band_results', __name__)


@band_results.route('/band_results')
def get_band_results():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
    return render_template('band_results.html', data="data", year_list=y_list)


@band_results.route('/_update_band_data')
def update_band_results():
    grade = request.args.get('grade', '1', type=str)
    band = request.args.get('band', '1', type=str)
    year_from = request.args.get('year_from', 2003, type=int)
    year_to = request.args.get('year_to', 2018, type=int)
    compare_band = request.args.get('comp_band', 'none', type=str)
    return jsonify(update_band_data(grade, band, compare_band, year_from, year_to))


@band_results.route('/_get_band_list')
def get_band_list():
    grade = request.args.get('grade', '1', type=str)
    year_from = request.args.get('year_from', 2003, type=int)
    year_to = request.args.get('year_to', 2018, type=int)
    return jsonify(get_bands_list(grade, year_from, year_to))

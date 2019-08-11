from flask import Blueprint, render_template, request, jsonify

from modules.generate_data.band_results.band_results import get_bands_list, update_band_data

band_results = Blueprint('band_results', __name__)


@band_results.route('/band_results')
def get_band_results():
    return render_template('band_results.html', data="data")


@band_results.route('/_update_band_data')
def update_band_results():
    grade = request.args.get('grade', '1', type=str)
    band = request.args.get('band', '1', type=str)
    compare_band = request.args.get('comp_band', 'none', type=str)
    return jsonify(update_band_data(grade, band, compare_band))


@band_results.route('/_get_band_list')
def get_band_list():
    grade = request.args.get('grade', '1', type=str)
    return jsonify(get_bands_list(grade))

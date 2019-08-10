from flask import Blueprint, render_template, request, jsonify

from modules.generate_data.band_results import get_bands_data, conv_key_to_str, add_missing_keys, get_bands_list

band_results = Blueprint('band_results', __name__)


@band_results.route('/band_results')
def get_band_results():
    return render_template('band_results.html', data="data")


@band_results.route('/_update_band_data')
def update_band_data():
    grade = request.args.get('grade', '1', type=str)
    band = request.args.get('band', '1', type=str)
    compare_band = request.args.get('comp_band', 'none', type=str)
    data = [[], []]
    if grade == '1':
        band_data = get_bands_data(grade, band)
        if compare_band == 'none':
            for k in band_data:
                graph_title = str(k[2]) + " Totals in Grade " + grade + " (2003-2018)"
                names, values = zip(*conv_key_to_str(k[1]).items())
                data[0].append([graph_title, [names, values], str(k[2])])
        else:
            compare_band_data = get_bands_data(grade, compare_band)
            for k in range(len(band_data)):
                add_missing_keys(band_data[k][1], compare_band_data[k][1])
                graph_title = str(band_data[k][2]) + " Totals in Grade " + grade + " (2003-2018)"
                names, values = zip(*conv_key_to_str(band_data[k][1]).items())
                data[0].append([graph_title, [names, values], str(band_data[k][2])])

                names, values = zip(*conv_key_to_str(compare_band_data[k][1]).items())
                data[1].append([graph_title, [names, values], str(compare_band_data[k][2])])
    else:
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
    return jsonify(data)


@band_results.route('/_get_band_list')
def get_band_list():
    grade = request.args.get('grade', '1', type=str)
    return jsonify(get_bands_list(grade))
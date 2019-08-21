from flask import Blueprint, render_template, request
from modules.shared.shared_functions import convert_grade
from modules.generate_data.major_wins.get_results import get_band_results, convert_result_type

major_wins = Blueprint('major_wins', __name__)


@major_wins.route('/major_totals')
def get_major_wins():
    y_list = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
    return render_template('major_wins.html', year_list=y_list)


@major_wins.route('/_get_grade_total')
def get_grade_total():
    grade = convert_grade(request.args.get('grade', '1', type=str))
    year_from = request.args.get('year_from', 2003, type=int)
    year_to = request.args.get('year_to', 2019, type=int)
    result_type = request.args.get('type', '1', type=str)
    graph_title = "Total Number of {0} Wins in Grade {1} ({2}-{3})".format(convert_result_type(result_type), grade,
                                                                           year_from, year_to)
    graph_data = get_band_results(str(grade), result_type, year_from, year_to)
    return {'data': graph_data, 'title': graph_title}

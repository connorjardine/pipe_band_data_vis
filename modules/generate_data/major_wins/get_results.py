from modules.generate_data.major_wins.grade1_results import get_grade1_results_totals
from modules.shared.shared_functions import convert_grade
from modules.generate_data.major_wins.other_results import *


def convert_result_type(result_type):
    if result_type == 'w':
        return "Overall"
    elif result_type == 'd':
        return "Drumming"
    elif result_type == 'e':
        return "Ensemble"
    elif result_type == 'p':
        return "Piping"


def get_g1_band_results(place_type, year_from, year_to):
    if year_from == 2003 and year_to == 2018:
        if place_type == 'w':
            names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_overall"})[0]['data']))
        elif place_type == 'd':
            names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_drumming"})[0]['data']))
        elif place_type == 'e':
            names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_ensemble"})[0]['data']))
        else:
            names, values = zip(*jsonpickle.decode(pull_data(helper_collection, {"type": "g1_piping"})[0]['data']))
    else:
        names, values = zip(*get_grade1_results_totals('1', place_type, year_from, year_to))
    return names, values


def get_band_results(grade, place, place_type, year_from, year_to):
    grade = convert_grade(grade)
    if grade == '1':
        return get_g1_band_results(place_type, year_from, year_to)
    else:
        names, values = zip(*return_other_placings_data(place, grade, place_type))
        return names, values




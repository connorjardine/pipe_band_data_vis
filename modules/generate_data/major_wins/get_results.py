from modules.generate_data.major_wins.grade1_results import get_grade1_results_totals
from modules.shared.shared_functions import convert_grade
from modules.generate_data.major_wins.other_results import *


def convert_result_type(result_type):
    return {
        'w': "Overall",
        'd': "Drumming",
        'e': "Ensemble",
        'p': "Piping"
    }.get(result_type)


def get_band_results(grade, place_type, year_from, year_to):
    grade = convert_grade(grade)
    if grade == '1':
        names, values = zip(*get_grade1_results_totals(place_type, year_from, year_to))
    else:
        names, values = zip(*return_other_placings_data( grade, place_type, year_from, year_to))
    return names, values





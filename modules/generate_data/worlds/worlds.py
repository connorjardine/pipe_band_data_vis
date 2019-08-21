from operator import itemgetter
import jsonpickle
from modules.shared.shared_functions import convert_grade, convert_band_name
from modules.db.db import *


def return_other_worlds_data(grade, year_from, year_to,):
    grade = convert_grade(grade)
    results = pull_data(competitions_collection, {'Grade': grade, 'contest': 'World Championships',
                                                  'year': {'$gte': year_from, '$lte': year_to}})

    output = {}
    worlds_roll = []
    unfreeze = jsonpickle.decode

    for i in results:
        comp = unfreeze(i['results'])
        worlds_roll.append([i['year'], i['Grade'], i['contest'], comp[0]['band'], comp[0]['total']])
        band = comp[0]
        if ' EP' in band['place']:
            band['place'] = band['place'].replace(' EP', '')
        band['band'] = convert_band_name(band['band'])
        if band['band'] not in output:
            output[band['band']] = {'1': 1}
        else:
            output[band['band']]['1'] += 1

    worlds_output = []
    for key, value in output.items():
        worlds_output.append([key, value['1']])

    return sorted(worlds_output, key=itemgetter(1), reverse=True), worlds_roll


def get_grade1_worlds_totals(year_from, year_to):
    results = pull_data(worlds_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    output = {}
    worlds_roll = []
    unfreeze = jsonpickle.decode
    for i in results:
        comp = unfreeze(i['results'])
        worlds_roll.append([i['year'], i['Grade'], i['contest'], comp[0]['band'], comp[0]['med_t'], comp[0]['msr_t'], comp[0]['final_t']])
        band = comp[0]
        if band['band'] not in output:
            output[band['band']] = {str(band['place']): 1}
        else:
            output[band['band']]['1'] += 1

    worlds_output = []
    for key, value in output.items():
        temp = [key, value['1']]
        worlds_output.append(temp)

    return sorted(worlds_output, key=itemgetter(1), reverse=True), worlds_roll


def get_worlds_data(grade, year_from, year_to):
    if grade == '1':
        return get_grade1_worlds_totals(year_from, year_to)
    else:
        return return_other_worlds_data(grade, year_from, year_to)


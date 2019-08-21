from operator import itemgetter
import jsonpickle
from modules.shared.shared_functions import convert_band_name, add_to_dct
from modules.db.db import *


def get_grade1_totals(year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte':  year_to}})
    worlds_results = pull_data(worlds_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte':  year_to}})

    unfreeze = jsonpickle.decode
    output = {}
    totals_output = []

    for i in results:
        band = unfreeze(i['results'])[0]
        band['band'] = convert_band_name(band['band'])
        if ' EP' in band['place']:
            band['place'] = band['place'].replace(' EP', '')
        if band['band'] not in output:
            output[band['band']] = {str(band['place']): 1}
        else:
            output[band['band']]['1'] += 1

    for i in worlds_results:
        band = unfreeze(i['results'])[0]
        band['band'] = convert_band_name(band['band'])
        if band['band'] not in output:
            output[band['band']] = {str(band['place']): 1}
        else:
            output[band['band']]['1'] += 1

    for key, value in output.items():
        temp = [key, value['1']]
        totals_output.append(temp)


    return sorted(totals_output, key=itemgetter(1), reverse=True)


def get_grade1_drumming_or_ensemble_totals(doe, year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR', 'year': {'$gte': year_from, '$lte': year_to}})

    output = {}
    unfreeze = jsonpickle.decode

    for i in results:
        comp = unfreeze(i['results'])
        doe_winner = next(item for item in comp if item[doe] == '1')
        output = add_to_dct(doe_winner, output)

    for i in worlds_med_results:
        comp = unfreeze(i['results'])
        doe_winner = next(item for item in comp if item[doe] == '1')
        output = add_to_dct(doe_winner, output)

    for i in worlds_msr_results:
        comp = unfreeze(i['results'])
        doe_winner = next(item for item in comp if item[doe] == '1')
        output = add_to_dct(doe_winner, output)

    drumming_ensemble_output = []
    for key, value in output.items():
        drumming_ensemble_output.append([key, value['1']])

    return sorted(drumming_ensemble_output, key=itemgetter(1), reverse=True)


def get_grade1_piping_totals(year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR', 'year': {'$gte': year_from, '$lte': year_to}})

    output = {}
    unfreeze = jsonpickle.decode

    for i in results:
        comp = unfreeze(i['results'])
        p1 = next(item for item in comp if item['p1'] == '1')
        p2 = next(item for item in comp if item['p1'] == '1')
        output = add_to_dct(p1, output)
        output = add_to_dct(p2, output)

    for i in worlds_med_results:
        comp = unfreeze(i['results'])
        p1 = next(item for item in comp if item['p1'] == '1')
        p2 = next(item for item in comp if item['p1'] == '1')
        output = add_to_dct(p1, output)
        output = add_to_dct(p2, output)

    for i in worlds_msr_results:
        comp = unfreeze(i['results'])
        p1 = next(item for item in comp if item['p1'] == '1')
        p2 = next(item for item in comp if item['p1'] == '1')
        output = add_to_dct(p1, output)
        output = add_to_dct(p2, output)

    piping_output = []
    for key, value in output.items():
        piping_output.append([key, value['1']])

    return sorted(piping_output, key=itemgetter(1), reverse=True)


def get_grade1_results_totals(result_type, year_from, year_to):
    if result_type == 'w':
        return get_grade1_totals(year_from, year_to)
    elif result_type == 'p':
        return get_grade1_piping_totals(year_from, year_to)
    if result_type == 'd':
        return get_grade1_drumming_or_ensemble_totals('d', year_from, year_to)
    if result_type == 'e':
        return get_grade1_drumming_or_ensemble_totals('e', year_from, year_to)



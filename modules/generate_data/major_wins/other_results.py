from operator import itemgetter

from modules.shared.shared_functions import add_to_dct, convert_band_name
from modules.db.db import *

import jsonpickle


def return_other_data(grade, year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': grade, 'year': {'$gte': year_from, '$lte': year_to}})

    output = {}
    unfreeze = jsonpickle.decode

    for i in results:
        band = unfreeze(i['results'])[0]
        band['band'] = convert_band_name(band['band'])
        if ' EP' in band['place']:
            band['place'] = band['place'].replace(' EP', '')
        if band['band'] not in output:
            output[band['band']] = {band['place']: 1}
        else:
            output[band['band']][band['place']] += 1

    wins_output = []
    for key, value in output.items():
        wins_output.append([key, value['1']])

    return sorted(wins_output, key=itemgetter(1), reverse=True)


def return_other_placings_data(grade, place_type, year_from, year_to):
    if place_type == 'w':
        return return_other_data(grade, year_from, year_to)

    results = pull_data(competitions_collection, {'Grade': grade, 'year': {'$gte': year_from, '$lte': year_to}})

    output = {}
    unfreeze = jsonpickle.decode

    if place_type == 'p':
        for i in results:
            comp = unfreeze(i['results'])
            p1 = next(item for item in comp if item['p1'] == '1')
            p2 = next(item for item in comp if item['p1'] == '1')
            output = add_to_dct(p1, output)
            output = add_to_dct(p2, output)
    else:
        for i in results:
            comp = unfreeze(i['results'])
            doe_winner = next(item for item in comp if item[place_type] == '1')
            output = add_to_dct(doe_winner, output)

    placings_output = []
    for key, value in output.items():
        placings_output.append([key, value['1']])

    return sorted(placings_output, key=itemgetter(1), reverse=True)


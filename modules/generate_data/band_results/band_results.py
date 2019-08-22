import jsonpickle

from collections import OrderedDict
from modules.db.db import *
from modules.shared.shared_functions import convert_grade, convert_band_name

grades_list = ['2', '3a', '3b', '4a', '4b', 'juv', 'Nov', 'Nov%20A', 'Nov%20B']

index_list = ['t', 'p', 'd', 'e']


def conv_key_to_str(dct):
    dct = {int(k): int(v) for k, v in dct.items()}
    for k in list(OrderedDict(sorted(dct.items())).keys()):
        if k == 1:
            dct['1st'] = dct.pop(k)
        elif k == 2:
            dct['2nd'] = dct.pop(k)
        elif k == 3:
            dct['3rd'] = dct.pop(k)
        else:
            dct[str(k) + 'th'] = dct.pop(k)
    return dct


def add_missing_keys(dct, otr_dct):
    for k in otr_dct.keys():
        if k not in dct.keys():
            dct[k] = 0
    return dct


def collate_overall(comp, dct):
    for k in comp:
        k['band'] = convert_band_name(k['band'])
        if ' EP' in k['place']:
            k['place'] = k['place'].replace(' EP', '')
        if k['band'] not in dct:
            dct[k['band']] = {k['place']: 1}
            if '1' not in dct[k['band']]:
                dct[k['band']].update({'1': 0})
        else:
            if k['place'] in dct[k['band']]:
                dct[k['band']][k['place']] += 1
            else:
                dct[k['band']].update({k['place']: 1})
    return dct


def collate_data(comp, dct, index):
    for k in comp:
        k['band'] = convert_band_name(k['band'])
        if k['band'] not in dct:
            dct[k['band']] = {k[index]: 1}
            if '1' not in dct[k['band']]:
                dct[k['band']].update({'1': 0})
        else:
            if k[index] in dct[k['band']]:
                dct[k['band']][k[index]] += 1
            else:
                dct[k['band']].update({k[index]: 1})
    return dct


def get_output_string(os):
    return {
        't': "Overall",
        'd': "Drumming",
        'e': "Ensemble",
        'p': "Piping"
    }.get(os)


def get_grade1_band_totals(index, year_from, year_to, req_band):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR',
                                                             'year': {'$gte': year_from, '$lte': year_to}})
    worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED',
                                                             'year': {'$gte': year_from, '$lte': year_to}})
    worlds_results = pull_data(worlds_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})

    output = {}
    output_string = get_output_string(index)
    unfreeze = jsonpickle.decode
    if index == 't':
        for i in worlds_results:
            comp = unfreeze(i['results'])
            for k in comp:
                k['band'] = convert_band_name(k['band'])
                if k['band'] not in output:
                    output[k['band']] = {str(k['place']): 1}
                    if '1' not in output[k['band']]:
                        output[k['band']].update({'1': 0})
                else:
                    if str(k['place']) in output[k['band']]:
                        output[k['band']][str(k['place'])] += 1
                    else:
                        output[k['band']].update({str(k['place']): 1})
        for i in results:
            output = collate_overall(unfreeze(i['results']), output)

    elif index == 'd' or index == 'e':
        for i in results:
            output = collate_data(unfreeze(i['results']), output, index)
        for i in worlds_med_results:
            output = collate_data(unfreeze(i['results']), output, index)
        for i in worlds_msr_results:
            output = collate_data(unfreeze(i['results']), output, index)

    elif index == 'p':
        for i in results:
            output = collate_data(unfreeze(i['results']), output, 'p1')
            output = collate_data(unfreeze(i['results']), output, 'p2')
        for i in worlds_med_results:
            output = collate_data(unfreeze(i['results']), output, 'p1')
            output = collate_data(unfreeze(i['results']), output, 'p2')
        for i in worlds_msr_results:
            output = collate_data(unfreeze(i['results']), output, 'p1')
            output = collate_data(unfreeze(i['results']), output, 'p2')

    output = {req_band: output[req_band]}

    new_output = []
    for key, value in output.items():
        new_output.append([key, value])

    new_output.append(output_string)

    return new_output


def return_other_band_data(grade, index, year_from, year_to, req_band):
    grade = convert_grade(grade)
    results = pull_data(competitions_collection, {'Grade': grade, 'year': {'$gte': year_from, '$lte': year_to}})

    output = {}
    output_string = get_output_string(index)

    if index == 't':
        for i in results:
            output = collate_overall(jsonpickle.decode(i['results']), output)
    elif index == 'd' or index == 'e':
        for i in results:
            output = collate_data(jsonpickle.decode(i['results']), output, index)
    elif index == 'p':
        for i in results:
            output = collate_data(jsonpickle.decode(i['results']), output, 'p1')
            output = collate_data(jsonpickle.decode(i['results']), output, 'p2')

    output = {req_band: output[req_band]}
    new_output = []

    for key, value in output.items():
        new_output.append([key, value])

    new_output.append(output_string)

    return new_output


def get_bands_list(grade, year_from, year_to):
    grade = convert_grade(grade)
    worlds_results = pull_data(worlds_collection, {'Grade': grade, 'year': {'$gte': year_from, '$lte': year_to}})
    results = pull_data(competitions_collection, {'Grade': grade, 'year': {'$gte': year_from, '$lte': year_to}})
    unfreeze = jsonpickle.decode
    band_list = []
    for i in results:
        comp = unfreeze(i['results'])
        for k in comp:
            k['band'] = convert_band_name(k['band'])
            if k['band'] not in band_list:
                band_list.append(k['band'])
    if grade == '1':
        for i in worlds_results:
            comp = unfreeze(i['results'])
            for k in comp:
                k['band'] = convert_band_name(k['band'])
                if k['band'] not in band_list:
                    band_list.append(k['band'])
    return band_list


def get_bands_data(grade, band, year_from, year_to):
    grade = convert_grade(grade)
    data = []
    if grade == '1':
        for i in index_list:
            data.append(get_grade1_band_totals(i, year_from, year_to, band))
        return data
    for i in index_list:
        data.append(return_other_band_data(grade, i, year_from, year_to, band))
    return data


def update_band_data(grade, band, compare_band, year_from, year_to):
    data = [[], []]
    band_data = get_bands_data(grade, band, year_from, year_to)
    if compare_band == 'none' or compare_band == "":
        for k in band_data:
            graph_title = "{0} Totals in Grade {1} ({2}-{3})".format(str(k[1]), grade, year_from, year_to)
            names, values = zip(*conv_key_to_str(k[0][1]).items())
            data[0].append([graph_title, [names, values], str(k[1])])
    else:
        compare_band_data = get_bands_data(grade, compare_band, year_from, year_to)
        for k in range(len(band_data)):
            band_data[k][0][1] = add_missing_keys(band_data[k][0][1], compare_band_data[k][0][1])
            graph_title = "{0} Totals in Grade {1} ({2}-{3})".format(str(band_data[k][1]), grade, year_from, year_to)

            names, values = zip(*conv_key_to_str(band_data[k][0][1]).items())
            data[0].append([graph_title, [names, values], str(band_data[k][1])])

            names, values = zip(*conv_key_to_str(compare_band_data[k][0][1]).items())
            data[1].append([graph_title, [names, values], str(compare_band_data[k][1])])
    return data






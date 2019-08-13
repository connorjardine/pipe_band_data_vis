import jsonpickle
import time


from collections import Counter, OrderedDict
from modules.db.db import *
from modules.shared.shared_functions import convert_grade


grades_list = ['2', '3a', '3b', '4a', '4b', 'juv', 'Nov', 'Nov%20A', 'Nov%20B']

index_list = ['t', 'p', 'd', 'e']

placings_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
gpol_comb = ['Strathclyde Police', 'Greater Glasgow Police Pipe Band', 'Glasgow Police']
shotts_comb = ['Shotts and Dykehead Caledonia', 'The House of Edgar - Shotts and Dykehead',
               'The House of Edgar Shotts and Dykehead']
sfu_comb = ['Simon Fraser University - Canada', 'Simon Fraser University']
skye_comb = ['The Glasgow Skye Association', 'Pheonix Honda Glasgow Skye']
vale_comb = ['Vale of Atholl', 'Robert Wiseman Dairies Vale of Atholl']
dut_comb = ['David Urquhart Travel', 'David Urquhart Travel Pipes and Drums']
fife_comb = ['Police Scotland Fife', 'Police Scotland Fife Pipe Band', 'Fife Constabulary']
slot_comb = ["St Laurence O\'Toole - Eire", "St. Laurence O\'Toole", "St Laurence O'Toole"]
boghall_comb = ['Peoples Ford Boghall and Bathgate Caledonia', 'Peoples Ford - Boghall and Bathgate Caledonia',
                'Boghall and Bathgate Caledonia']
lb_comb = ['Lothian and Borders Police', 'Lothian and borders Police']

comb_list = [gpol_comb, shotts_comb, sfu_comb, skye_comb, vale_comb, dut_comb, fife_comb, slot_comb, boghall_comb,
             lb_comb]
non_comb_list = ['Field Marshal Montgomery', 'Scottish Power', 'Dysart and Dundonald', 'Ravara', 'Ballycoan',
                 'Bucksburn and District', 'Grampian Police', 'Glasgow Pipes and Drums', 'The Clan Gregor Society',
                 'Bleary and District', 'Ballinderry Bridge', 'New Zealand Police', 'City of Blacktown',
                 'Tayside Police', 'Cullybackey', 'Torphichen and Bathgate', 'Bagad Cap Caval',
                 'Inveraray and District', 'Toronto Police', 'Seven Towers', 'Denny and Dunipace Gleneagles',
                 'Spirit of Scotland', 'Dowco Triumph Street - Canada', 'Johnstone',
                 'Pipes and Drums of the Police Service of Northern Ireland', 'Buchan Peterson', 'Lomond and Clyde']


def comb_bands(b_comb, dct):
    b_counter = Counter()
    for j in b_comb:
        b_counter += Counter(dct.get(str(j)))
    upd_one = dict(b_counter)
    if '1' not in upd_one:
        upd_one.update({'1': 0})
    return b_comb[0], upd_one


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
        if k['band'] not in dct:
            if ' EP' in k['place']:
                k['place'] = k['place'].replace(' EP', '')
            dct[k['band']] = {k['place']: 1}
            if '1' not in dct[k['band']]:
                dct[k['band']].update({'1': 0})
        else:
            if ' EP' in k['place']:
                k['place'] = k['place'].replace(' EP', '')
            if k['place'] in dct[k['band']]:
                dct[k['band']][k['place']] += 1
            else:
                dct[k['band']].update({k['place']: 1})


def collate_data(comp, dct, index):
    for k in comp:
        if k['band'] not in dct:
            dct[k['band']] = {k[index]: 1}
            if '1' not in dct[k['band']]:
                dct[k['band']].update({'1': 0})
        else:
            if k[index] in dct[k['band']]:
                dct[k['band']][k[index]] += 1
            else:
                dct[k['band']].update({k[index]: 1})


def get_grade1_band_totals(index, year_from, year_to, req_band=None):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    output = {}
    output_string = ""
    if index == 't':
        output_string = "Overall"
        for i in pull_data(worlds_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}}):
            comp = jsonpickle.decode(i['results'])
            for k in comp:
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
            collate_overall(jsonpickle.decode(i['results']), output)

    elif index == 'd' or index == 'e':
        for i in results:
            collate_data(jsonpickle.decode(i['results']), output, index)
        for i in pull_data(competitions_collection, {'Grade': '1MED', 'year': {'$gte': year_from, '$lte': year_to}}):
            collate_data(jsonpickle.decode(i['results']), output, index)
        for i in pull_data(competitions_collection, {'Grade': '1MSR', 'year': {'$gte': year_from, '$lte': year_to}}):
            collate_data(jsonpickle.decode(i['results']), output, index)
        if index == 'd':
            output_string = "Drumming"
        else:
            output_string = "Ensemble"
    elif index == 'p':
        output_string = "Piping"
        for i in results:
            collate_data(jsonpickle.decode(i['results']), output, 'p1')
            collate_data(jsonpickle.decode(i['results']), output, 'p2')
        for i in pull_data(competitions_collection, {'Grade': '1MED', 'year': {'$gte': year_from, '$lte': year_to}}):
            collate_data(jsonpickle.decode(i['results']), output, 'p1')
            collate_data(jsonpickle.decode(i['results']), output, 'p2')
        for i in pull_data(competitions_collection, {'Grade': '1MSR', 'year': {'$gte': year_from, '$lte': year_to}}):
            collate_data(jsonpickle.decode(i['results']), output, 'p1')
            collate_data(jsonpickle.decode(i['results']), output, 'p2')

    combined_results = []
    for band in comb_list:
        combined_results.append(comb_bands(band, output))

    for band in non_comb_list:
        combined_results.append((band, output.get(str(band))))

    if req_band:
        for i in combined_results:
            if i[0] == req_band:
                if i[1]['1'] == 0:
                    del i[1]['1']
                i += (output_string,)
                return i
    return combined_results


def return_other_band_data(grade, index, year_from, year_to, req_band=None, contest=None):
    grade = convert_grade(grade)
    if contest is not None:
        results = pull_data(competitions_collection, {'Grade': grade, 'year': {'$gte': year_from, '$lte': year_to},
                                                      'contest': contest})
    else:
        results = pull_data(competitions_collection, {'Grade': grade, 'year': {'$gte': year_from, '$lte': year_to}})
    output = {}
    output_string = ""
    if index == 't':
        output_string = "Overall"
        for i in results:
            collate_overall(jsonpickle.decode(i['results']), output)
    elif index == 'd' or index == 'e':
        for i in results:
            collate_data(jsonpickle.decode(i['results']), output, index)
        if index == 'd':
            output_string = "Drumming"
        else:
            output_string = "Ensemble"
    elif index == 'p':
        output_string = "Piping"
        for i in results:
            collate_data(jsonpickle.decode(i['results']), output, 'p1')
            collate_data(jsonpickle.decode(i['results']), output, 'p2')

    new_output = []
    for key, value in output.items():
        new_output.append([key, value])

    merge_list = []
    for band in new_output:
        for i in comb_list:
            if band[0] in i:
                latch = True
                for k in merge_list:
                    if i[0] == k[0]:
                        k[1] = dict(Counter(k[1]) + Counter(band[1]))
                        latch = False
                        break
                    latch = True
                if latch is True:
                    merge_list.append([i[0], band[1]])
                new_output.remove(band)

    if req_band:
        new_output += merge_list
        for i in new_output:
            if i[0] == req_band:
                if i[1]['1'] == 0:
                    del i[1]['1']
                i += (output_string,)
                return i
    return new_output


def get_bands_list(grade, year_from, year_to):
    grade = convert_grade(grade)
    output_list = []
    if grade == '1':
        for k in get_grade1_band_totals('t', year_from, year_to):
            output_list.append(k[0])
    if grade in grades_list:
        for k in return_other_band_data(grade, 't', year_from, year_to):
            output_list.append(k[0])
    output_list.sort()
    return output_list


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
    if compare_band == 'none':
        for k in band_data:
            graph_title = "{0} Totals in Grade {1} ({2}-{3})".format(str(k[2]), grade, year_from, year_to)

            names, values = zip(*conv_key_to_str(k[1]).items())
            data[0].append([graph_title, [names, values], str(k[2])])
    else:
        compare_band_data = get_bands_data(grade, compare_band, year_from, year_to)
        for k in range(len(band_data)):
            add_keys = add_missing_keys(band_data[k][1], compare_band_data[k][1])
            add_keys_list = list(band_data[k])
            add_keys_list[1] = add_keys
            band_data[k] = tuple(add_keys_list)
            graph_title = "{0} Totals in Grade {1} ({2}-{3})".format(str(band_data[k][2]), grade, year_from, year_to)

            names, values = zip(*conv_key_to_str(band_data[k][1]).items())
            data[0].append([graph_title, [names, values], str(band_data[k][2])])

            names, values = zip(*conv_key_to_str(compare_band_data[k][1]).items())
            data[1].append([graph_title, [names, values], str(compare_band_data[k][2])])
    return data









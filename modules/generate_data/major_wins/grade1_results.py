import jsonpickle

from collections import Counter
from modules.sort import *
from modules.db.db import *


results = pull_data(competitions_collection, {'Grade': '1'})
worlds_results = pull_data(worlds_collection, {'Grade': '1'})
worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR'})
worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED'})

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


def get_grade1_totals(place, year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte':  year_to}})
    worlds_results = pull_data(worlds_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte':  year_to}})
    output = {}
    for i in results:
        collate_overall(jsonpickle.decode(i['results']), output)
    for i in worlds_results:
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

    combined_results = []
    for band in comb_list:
        combined_results.append(comb_bands(band, output))

    for band in non_comb_list:
        if output.get(str(band)) is None:
            combined_results.append((band, {}))
        else:
            combined_results.append((band, output.get(str(band))))

    for i in combined_results:
        for k in placings_list:
            if i[1] is not None and k not in i[1]:
                i[1].update({k: 0})

    firsts = []

    for i in combined_results:
        if i[1] is not None and i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results


def get_grade1_drumming_totals(place, year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR', 'year': {'$gte': year_from, '$lte': year_to}})
    output = {}
    for i in results:
        collate_data(jsonpickle.decode(i['results']), output, 'd')
    for i in worlds_med_results:
        collate_data(jsonpickle.decode(i['results']), output, 'd')
    for i in worlds_msr_results:
        collate_data(jsonpickle.decode(i['results']), output, 'd')

    combined_results = []
    for band in comb_list:
        combined_results.append(comb_bands(band, output))
    for band in non_comb_list:
        if output.get(str(band)) is None:
            combined_results.append((band, {}))
        else:
            combined_results.append((band, output.get(str(band))))
    for i in combined_results:
        for k in placings_list:
            if k not in i[1]:
                i[1].update({k: 0})

    firsts = []
    for i in combined_results:
        if i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results


def get_grade1_ensemble_totals(place, year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR', 'year': {'$gte': year_from, '$lte': year_to}})
    output = {}
    for i in results:
        collate_data(jsonpickle.decode(i['results']), output, 'e')
    for i in worlds_med_results:
        collate_data(jsonpickle.decode(i['results']), output, 'e')
    for i in worlds_msr_results:
        collate_data(jsonpickle.decode(i['results']), output, 'e')

    combined_results = []
    for band in comb_list:
        combined_results.append(comb_bands(band, output))
    for band in non_comb_list:
        if output.get(str(band)) is None:
            combined_results.append((band, {}))
        else:
            combined_results.append((band, output.get(str(band))))
    for i in combined_results:
        for k in placings_list:
            if k not in i[1]:
                i[1].update({k: 0})

    firsts = []
    for i in combined_results:
        if i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results


def get_grade1_piping_totals(place, year_from, year_to):
    results = pull_data(competitions_collection, {'Grade': '1', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED', 'year': {'$gte': year_from, '$lte': year_to}})
    worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR', 'year': {'$gte': year_from, '$lte': year_to}})
    output = {}
    for i in results:
        collate_data(jsonpickle.decode(i['results']), output, 'p1')
        collate_data(jsonpickle.decode(i['results']), output, 'p2')
    for i in worlds_med_results:
        collate_data(jsonpickle.decode(i['results']), output, 'p1')
        collate_data(jsonpickle.decode(i['results']), output, 'p2')
    for i in worlds_msr_results:
        collate_data(jsonpickle.decode(i['results']), output, 'p1')
        collate_data(jsonpickle.decode(i['results']), output, 'p2')

    combined_results = []
    for band in comb_list:
        combined_results.append(comb_bands(band, output))
    for band in non_comb_list:
        if output.get(str(band)) is None:
            combined_results.append((band, {}))
        else:
            combined_results.append((band, output.get(str(band))))
    for i in combined_results:
        for k in placings_list:
            if k not in i[1]:
                i[1].update({k: 0})

    firsts = []
    for i in combined_results:
        if i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results


def get_grade1_results_totals(place, result_type, year_from, year_to):
    if result_type == 'w':
        return get_grade1_totals(place, year_from, year_to)
    elif result_type == 'p':
        return get_grade1_piping_totals(place, year_from, year_to)
    if result_type == 'd':
        return get_grade1_drumming_totals(place, year_from, year_to)
    if result_type == 'e':
        return get_grade1_ensemble_totals(place, year_from, year_to)


# find_and_mod(helper_collection, {"type": "g1_piping"}, {"type": "g1_piping",
# "data": jsonpickle.encode(get_grade1_piping_totals('1', 2003, 2019))})

# find_and_mod(helper_collection, {"type": "g1_drumming"}, {"type": "g1_drumming",
# "data": jsonpickle.encode(get_grade1_drumming_totals('1', 2003, 2019))})

# find_and_mod(helper_collection, {"type": "g1_totals"}, {"type": "g1_totals",
#    "data": jsonpickle.encode(get_grade1_totals('1', 2003, 2019))})

# find_and_mod(helper_collection, {"type": "g1_ensemble"}, {"type": "g1_ensemble",
#    "data": jsonpickle.encode(get_grade1_ensemble_totals('1', 2003, 2019))})


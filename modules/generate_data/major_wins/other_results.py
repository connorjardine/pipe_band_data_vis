from collections import Counter
from modules.sort import *
from modules.db.db import *

import jsonpickle


placings_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                 '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']

wat = ['George Watsons College', "George Watson's College", "George Watson's College - Juvenile",
       "George Watson's College - Novice"]
bog_juv = ['Boghall and Bathgate Caledonia', 'Peoples Ford - Boghall and Bathgate Caledonia']
dol = ['Dollar Academy', 'Dollar Academy (No. 2)']
coa = ['Coalburn I.O.R.', 'Coalburn I.O.R']
buc = ['Buchan Peterson', 'Buchan']

comb_list = [wat, bog_juv, dol, coa]


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


def comb_bands(b_comb, dct):
    b_counter = Counter()
    for j in b_comb:
        b_counter += Counter(dct.get(str(j)))
    upd_one = dict(b_counter)
    if '1' not in upd_one:
        upd_one.update({'1': 0})
    return b_comb[0], upd_one


def return_other_data(place, grade, contest=None):

    if contest is not None:
        results = pull_data(competitions_collection, {'Grade': grade, 'contest': contest})
    else:
        results = pull_data(competitions_collection, {'Grade': grade})
    output = {}

    for i in results:
        comp = jsonpickle.decode(i['results'])
        for k in comp:
            if k['band'] not in output:
                if ' EP' in k['place']:
                    k['place'] = k['place'].replace(' EP', '')
                output[k['band']] = {k['place']: 1}
                if '1' not in output[k['band']]:
                    output[k['band']].update({'1': 0})
            else:
                k['place'] = k['place'].replace(' EP', '')
                if k['place'] in output[k['band']]:
                    output[k['band']][k['place']] += 1
                else:
                    output[k['band']].update({k['place']: 1})

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

    new_output += merge_list
    for i in new_output:
        for k in placings_list:
            if k not in i[1]:
                i[1].update({k: 0})

    firsts = []
    for i in new_output:
        if i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results


def return_other_placings_data(place, grade, place_type, contest=None):
    if place_type == 'w':
        return return_other_data(place, grade)
    if contest is not None:
        results = pull_data(competitions_collection, {'Grade': grade, 'contest': contest})
    else:
        results = pull_data(competitions_collection, {'Grade': grade})

    output = {}
    if place_type == 'p':
        for i in results:
            collate_data(jsonpickle.decode(i['results']), output, 'p1')
            collate_data(jsonpickle.decode(i['results']), output, 'p2')
    else:
        for i in results:
            collate_data(jsonpickle.decode(i['results']), output, place_type)

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

    new_output += merge_list

    for i in new_output:
        for k in placings_list:
            if k not in i[1]:
                i[1].update({k: 0})

    firsts = []
    for i in new_output:
        if i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results

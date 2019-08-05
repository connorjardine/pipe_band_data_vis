import jsonpickle

from collections import Counter, OrderedDict
from modules.db.db import *

worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR'})
worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED'})


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
    dct = {int(k):int(v) for k,v in dct.items()}
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


def convert_grade(grade):
    if grade == 'Juv':
        grade = 'juv'
    if grade == 'Nov A':
        grade = 'Nov%20A'
    if grade == 'Nov B':
        grade = 'Nov%20B'
    return grade


def get_grade1_band_totals(index, req_band=None):
    results = pull_data(competitions_collection, {'Grade': '1'})
    output = {}
    output_string = ""
    if index == 't':
        output_string = "Overall"
        for i in pull_data(worlds_collection, {'Grade': '1'}):
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
        for i in worlds_med_results:
            collate_data(jsonpickle.decode(i['results']), output, index)
        for i in worlds_msr_results:
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
        combined_results.append((band, output.get(str(band))))

    if req_band:
        for i in combined_results:
            if i[0] == req_band:
                if i[1]['1'] == 0:
                    del i[1]['1']
                i += (output_string,)
                return i
    return combined_results


def return_other_band_data(grade, index, req_band=None, contest=None):
    grade = convert_grade(grade)
    if contest is not None:
        results = pull_data(competitions_collection, {'Grade': grade, 'contest': contest})
    else:
        results = pull_data(competitions_collection, {'Grade': grade})
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
            output_string = "Piping"
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


def get_bands_list(grade):
    grade = convert_grade(grade)
    output_list = []
    if grade == '1':
        for k in get_grade1_band_totals('t'):
            output_list.append(k[0])
    if grade in grades_list:
        for k in return_other_band_data(grade, 't'):
            output_list.append(k[0])
    return output_list


def get_bands_data(grade, band):
    grade = convert_grade(grade)
    data = []
    if grade == '1':
        for i in index_list:
            data.append(get_grade1_band_totals(i, band))
        return data
    for i in index_list:
        data.append(return_other_band_data(grade, i, band))
    return data


import pymongo
import jsonpickle

from collections import Counter
from modules.sort import *

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
competitions_collection = db.competitions
worlds_collection = db.worlds
worlds_results = worlds_collection.find({'Grade': '1'})
worlds_msr_results = competitions_collection.find({'Grade': '1MSR'})
worlds_med_results = competitions_collection.find({'Grade': '1MED'})

helper_collection = db.band_helper_data

grades_list = ['2', '3a', '3b', '4a', '4b', 'juv', 'Nov', 'Nov%20A', 'Nov%20B']

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


def get_grade1_band_totals(req_band=None):
    results = competitions_collection.find({'Grade': '1'})
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
        combined_results.append((band, output.get(str(band))))

    if req_band:
        for i in combined_results:
            if i[0] == req_band:
                if i[1]['1'] == 0:
                    del i[1]['1']
                return i

    return combined_results


def return_other_band_data(grade, req_band=None, contest=None):

    if contest is not None:
        results = competitions_collection.find({'Grade': grade, 'contest': contest})
    else:
        results = competitions_collection.find({'Grade': grade})
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

    if req_band:
        new_output += merge_list
        for i in new_output:
            if i[0] == req_band:
                if i[1]['1'] == 0:
                    del i[1]['1']
                return i

    return new_output


def get_bands_list(grade):
    if grade == 'Nov A':
        grade = 'Nov%20A'
    if grade == 'Nov B':
        grade = 'Nov%20B'
    output_list = []
    if grade == '1':
        for k in get_grade1_band_totals():
            output_list.append(k[0])
    if grade in grades_list:
        for k in return_other_band_data(grade):
            output_list.append(k[0])
    return output_list


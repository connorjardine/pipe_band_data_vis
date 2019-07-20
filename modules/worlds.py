import pymongo
import jsonpickle
from collections import Counter
from modules.sort import *

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
competitions_collection = db.competitions
worlds_collection = db.worlds

placings_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                 '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
wat = ['George Watsons College', "George Watson's College", "George Watson's College - Juvenile",
       "George Watson's College - Novice"]
bog_juv = ['Boghall and Bathgate Caledonia', 'Peoples Ford - Boghall and Bathgate Caledonia']
dol = ['Dollar Academy', 'Dollar Academy (No. 2)']
coa = ['Coalburn I.O.R.', 'Coalburn I.O.R']
buc = ['Buchan Peterson', 'Buchan']

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

other_comb_list = [wat, bog_juv, dol, coa]

comb_list = [gpol_comb, shotts_comb, sfu_comb, skye_comb, vale_comb, dut_comb, fife_comb, slot_comb, boghall_comb,
             lb_comb]
non_comb_list = ['Field Marshal Montgomery', 'Scottish Power', 'Dysart and Dundonald', 'Ravara', 'Ballycoan',
                 'Bucksburn and District', 'Grampian Police', 'Glasgow Pipes and Drums', 'The Clan Gregor Society',
                 'Bleary and District', 'Ballinderry Bridge', 'New Zealand Police', 'City of Blacktown',
                 'Tayside Police', 'Cullybackey', 'Torphichen and Bathgate', 'Bagad Cap Caval',
                 'Inveraray and District', 'Toronto Police', 'Seven Towers', 'Denny and Dunipace Gleneagles',
                 'Spirit of Scotland', 'Dowco Triumph Street - Canada', 'Johnstone',
                 'Pipes and Drums of the Police Service of Northern Ireland', 'Buchan Peterson', 'Lomond and Clyde']


def collate_overall(comp, dct):
    for k in comp:
        if k['band'] not in dct:
            dct[k['band']] = {str(k['place']): 1}
            if '1' not in dct[k['band']]:
                dct[k['band']].update({'1': 0})
        else:
            if str(k['place']) in dct[k['band']]:
                dct[k['band']][str(k['place'])] += 1
            else:
                dct[k['band']].update({str(k['place']): 1})


def comb_bands(b_comb, dct):
    b_counter = Counter()
    for j in b_comb:
        b_counter += Counter(dct.get(str(j)))
    upd_one = dict(b_counter)
    if '1' not in upd_one:
        upd_one.update({'1': 0})
    return b_comb[0], upd_one


def return_other_worlds_data(place, grade, contest=None):
    if grade == 'Juv':
        grade = 'juv'
    if grade == 'Nov A':
        grade = 'Nov%20A'
    if grade == 'Nov B':
        grade = 'Nov%20B'

    if contest is not None:
        results = competitions_collection.find({'Grade': grade, 'contest': contest})
    else:
        results = competitions_collection.find({'Grade': grade})

    output = {}
    worlds_roll = []

    for i in results:
        comp = jsonpickle.decode(i['results'])
        worlds_roll.append([i['year'], i['Grade'], i['contest'], comp[0]['band'], comp[0]['total']])
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
        for i in other_comb_list:
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
    return final_results, worlds_roll


def get_grade1_worlds_totals(place):
    results = worlds_collection.find({'Grade': '1'})

    output = {}
    worlds_roll = []

    for i in results:
        comp = jsonpickle.decode(i['results'])
        worlds_roll.append([i['year'], i['Grade'], i['contest'], comp[0]['band'], comp[0]['med_t'], comp[0]['msr_t'], comp[0]['final_t']])
        collate_overall(comp, output)

    combined_results = []
    for band in comb_list:
        combined_results.append(comb_bands(band, output))

    for band in non_comb_list:
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
    return final_results, worlds_roll



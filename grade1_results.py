import pymongo
import jsonpickle

from collections import Counter

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
competitions_collection = db.competitions
worlds_collection = db.worlds
results = competitions_collection.find({'Grade': '1'})
worlds_results = worlds_collection.find({'Grade': '1'})

output = {}

placings_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
gpol_comb = ['Glasgow Police', 'Strathclyde Police', 'Greater Glasgow Police Pipe Band']
shotts_comb = ['Shotts and Dykehead Caledonia', 'The House of Edgar - Shotts and Dykehead',
               'The House of Edgar Shotts and Dykehead']
sfu_comb = ['Simon Fraser University - Canada', 'Simon Fraser University']
skye_comb = ['The Glasgow Skye Association', 'Pheonix Honda Glasgow Skye']
vale_comb = ['Vale of Atholl', 'Robert Wiseman Dairies Vale of Atholl']
dut_comb = ['David Urquhart Travel', 'David Urquhart Travel Pipes and Drums']
fife_comb = ['Police Scotland Fife', 'Police Scotland Fife Pipe Band', 'Fife Constabulary']
slot_comb = ["St Laurence O\'Toole - Eire", "St. Laurence O\'Toole"]
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


def comb_bands(b_comb):
    b_counter = Counter()
    for j in b_comb:
        b_counter += Counter(output[j])
    upd_one = dict(b_counter)
    if '1' not in upd_one:
        upd_one.update({'1': 0})
    return b_comb[0], upd_one


combined_results = []
for band in comb_list:
    combined_results.append(comb_bands(band))

for band in non_comb_list:
    combined_results.append((band, output[band]))

for i in combined_results:
    for k in placings_list:
        if k not in i[1]:
            i[1].update({k: 0})


def partition(arr, low, high, index):
    i = (low - 1)
    pivot = arr[high][1][index]

    for j in range(low, high):
        if arr[j][1][index] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high, index):
    if low < high:
        pi = partition(arr, low, high, index)
        quick_sort(arr, low, pi - 1, index)
        quick_sort(arr, pi + 1, high, index)


def return_g1_data(place):
    firsts = []

    for i in combined_results:
        if i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results



from operator import add

from modules.generate_data.coc import *
from modules.db.db import *

placings_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
gpol_comb = ['Glasgow Police', 'Strathclyde Police', 'Greater Glasgow Police Pipe Band']
shotts_comb = ['Shotts and Dykehead Caledonia', 'The House of Edgar - Shotts and Dykehead',
               'The House of Edgar Shotts and Dykehead']
sfu_comb = ['Simon Fraser University - Canada', 'Simon Fraser University']
skye_comb = ['The Glasgow Skye Association', 'Pheonix Honda Glasgow Skye']
vale_comb = ['Vale of Atholl', 'Robert Wiseman Dairies Vale of Atholl']
dut_comb = ['David Urquhart Travel', 'David Urquhart Travel Pipes and Drums']
fife_comb = ['Police Scotland Fife', 'Police Scotland Fife Pipe Band', 'Fife Constabulary']
slot_comb = ["St Laurence O\'Toole - Eire", "St. Laurence O\'Toole", "St.Laurence O\'Toole", "St Laurence O'Toole"]
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
    upd_one = []
    for j in b_comb:
        if not upd_one:
            upd_one = dct[j]
        else:
            upd_one = list(map(add, upd_one, dct[j]))
    return b_comb[0], upd_one


def line_coc():
    it = 0
    output = {}
    for i in range(2003, 2019):
        for k in get_coc('1', i)[::-1]:
            if k[0] not in output:
                output[k[0]] = [0] * 18
                output[k[0]][it] = k[1]
            else:
                output[k[0]][it] = k[1]
        it += 1

    combined_results = []
    for band in comb_list:
        new_comb = comb_bands(band, output)
        if sum(new_comb[1]) is not 0:
            combined_results.append(new_comb)

    for band in non_comb_list:
        if sum(output[band]) is not 0:
            combined_results.append((band, output[band]))

    for k in combined_results:
        del k[1][-2:]
        for i in range(len(k[1])):
            if i != 0 and i != len(k[1]) - 1:
                if (k[1][i - 1] == 0 and k[1][i + 1] == 0) or (k[1][i - 1] is None and k[1][i + 1] == 0) or (
                        k[1][i - 1] == 0 and k[1][i + 1] is None) or (
                        k[1][i - 1] == 0 and i == len(k[1])-2):
                    if k[1][i] == 0:
                        k[1][i] = None
            if i == len(k[1]) - 1 and (k[1][i-1] == 0 or k[1][i-1] is None):
                if k[1][i] == 0:
                    k[1][i] = None
            if i == 0 and (k[1][i+1] == 0 or k[1][i+1] is None):
                if k[1][i] == 0:
                    k[1][i] = None
    return combined_results


def line_drumming_coc():
    it = 0
    output = {}
    for i in range(2003, 2019):
        for k in get_drumming_coc('1', i)[::-1]:
            if k[0] not in output:
                output[k[0]] = [0] * 18
                output[k[0]][it] = k[1]
            else:
                output[k[0]][it] = k[1]
        it += 1

    combined_results = []
    for band in comb_list:
        new_comb = comb_bands(band, output)
        if sum(new_comb[1]) is not 0:
            combined_results.append(new_comb)

    for band in non_comb_list:
        if sum(output[band]) is not 0:
            combined_results.append((band, output[band]))

    for k in combined_results:
        del k[1][-2:]
        for i in range(len(k[1])):
            if i != 0 and i != len(k[1]) - 1:
                if (k[1][i - 1] == 0 and k[1][i + 1] == 0) or (k[1][i - 1] is None and k[1][i + 1] == 0) or (
                        k[1][i - 1] == 0 and k[1][i + 1] is None) or (
                        k[1][i - 1] == 0 and i == len(k[1])-2):
                    if k[1][i] == 0:
                        k[1][i] = None
            if i == len(k[1]) - 1 and (k[1][i-1] == 0 or k[1][i-1] is None):
                if k[1][i] == 0:
                    k[1][i] = None
            if i == 0 and (k[1][i+1] == 0 or k[1][i+1] is None):
                if k[1][i] == 0:
                    k[1][i] = None
    return combined_results


#helper_collection.insert_one({"type": "g1_drumming_coc", "data": jsonpickle.encode(line_drumming_coc())})
#helper_collection.insert_one({"type": "g1_coc", "data": jsonpickle.encode(line_coc())})

import jsonpickle
from modules.db.db import *

grades_list = ['2', '3a', '3b', '4a', '4b', 'juv', 'Nov', 'Nov%20A', 'Nov%20B']


def get_slams():
    slams = []
    for i in range(2003, 2020):
        results = pull_data(competitions_collection, {'Grade': '1', 'year': i})
        worlds_results = pull_data(worlds_collection, {'Grade': '1', 'year': i})

        winning_band = ""
        for k in worlds_results:
            winning_band = jsonpickle.decode(k['results'])[0]['band']
        latch = True
        for n in results:
            if jsonpickle.decode(n['results'])[0]['band'] != winning_band:
                latch = False
        if latch:
            slams.append([i, '1', winning_band])
        for k in grades_list:
            results = pull_data(competitions_collection, {'Grade': k, 'year': i})
            winning_band = ""
            latch = True
            for n in results:
                if winning_band is "":
                    winning_band = jsonpickle.decode(n['results'])[0]['band']
                elif jsonpickle.decode(n['results'])[0]['band'] != winning_band:
                    latch = False
            if latch:
                if winning_band is not "":
                    if k == 'juv':
                        k = 'Juv'
                    slams.append([i, k, winning_band])
    return slams


# push_data(helper_collection, {"type": "slams", "data": jsonpickle.encode((get_slams()))})
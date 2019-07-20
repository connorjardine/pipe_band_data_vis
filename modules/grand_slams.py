import pymongo
import jsonpickle

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
competitions_collection = db.competitions
worlds_collection = db.worlds
helper_collection = db.band_helper_data

grades_list = ['2', '3a', '3b', '4a', '4b', 'juv', 'Nov', 'Nov%20A', 'Nov%20B']


def get_slams():
    slams = []
    for i in range(2003,2019):
        results = competitions_collection.find({'Grade': '1', 'year': i})
        worlds_results = worlds_collection.find({'Grade': '1', 'year': i})

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
            results = competitions_collection.find({'Grade': k, 'year': i})
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


#helper_collection.insert_one({"type": "slams", "data": jsonpickle.encode((get_slams()))})
import pymongo

competitions_collection = "competitions"
worlds_collection = "worlds"
helper_collection = "band"

settings = "connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1"


def pull_data(collection, data=None):
    if collection == "competitions":
        client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority").rspba.competitions
    elif collection == "worlds":
        client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority").rspba.worlds
    else:
        client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority").rspba.band_helper_data
    if not data:
        output = client.find()
    else:
        output = client.find(data)
    return output








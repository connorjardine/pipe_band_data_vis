import pymongo

competitions_collection = "competitions"
worlds_collection = "worlds"
helper_collection = "band"


def pull_data(collection, data=None):
    if collection == "competitions":
        client = pymongo.MongoClient("mongodb+srv://read:readaccess@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.competitions
    elif collection == "worlds":
        client = pymongo.MongoClient("mongodb+srv://read:readaccess@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.worlds
    else:
        client = pymongo.MongoClient("mongodb+srv://read:readaccess@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.band_helper_data
    if not data:
        output = client.find()
    else:
        output = client.find(data)
    return output


def push_data(collection, data):
    if collection == "competitions":
        client = pymongo.MongoClient("mongodb+srv://read:readaccess@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.competitions
    elif collection == "worlds":
        client = pymongo.MongoClient("mongodb+srv://read:readaccess@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.worlds
    else:
        client = pymongo.MongoClient("mongodb+srv://write:Write97@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.band_helper_data
    client.insert_one(data)


def find_and_mod(collection, data, update_data):
    if collection == "competitions":
        client = pymongo.MongoClient("mongodb+srv://read:readaccess@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.competitions
    elif collection == "worlds":
        client = pymongo.MongoClient("mongodb+srv://read:readaccess@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.worlds
    else:
        client = pymongo.MongoClient("mongodb+srv://write:Write97@connor-5cmei.mongodb.net/test?retryWrites=true&w"
                                     "=majority", connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                                     connect=False, maxPoolsize=1).rspba.band_helper_data
    client.find_and_modify(query=data, update={"$set": update_data}, upsert=False, full_response= True)






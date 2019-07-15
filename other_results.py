import pymongo
import jsonpickle

from collections import Counter

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
competitions_collection = db.competitions
worlds_collection = db.worlds

placings_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                 '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']


def return_other_data(place, grade, contest=None):

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

    for i in new_output:
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

    firsts = []
    for i in new_output:
        if i[1][place] > 0:
            firsts += [i]

    quick_sort(firsts, 0, len(firsts)-1, place)

    final_results = []
    for k in firsts[::-1]:
        final_results += [[k[0], k[1][place]]]

    return final_results


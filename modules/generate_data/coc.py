import jsonpickle
from modules.db.db import *

coc_weightings = {'1': 6, '2': 5, '3': 4, '4': 3, '5': 2, '6': 1}


def partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high][1]

    for j in range(low, high):
        if arr[j][1] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


def get_coc(grade, year):

    results = pull_data(competitions_collection, {'Grade': grade, 'year': year})
    worlds_results = pull_data(worlds_collection, {'Grade': grade, 'year': year})
    output = {}

    for i in results:
        comp = jsonpickle.decode(i['results'])
        for k in comp:
            if k['band'] not in output:
                if ' EP' in k['place']:
                    k['place'] = k['place'].replace(' EP', '')
                if k['place'] in coc_weightings:
                    output[k['band']] = coc_weightings[k['place']]
                else:
                    output[k['band']] = 0
            else:
                if ' EP' in k['place']:
                    k['place'] = k['place'].replace(' EP', '')
                if k['place'] in coc_weightings:
                    output[k['band']] = output[k['band']] + coc_weightings[k['place']]

    if grade == '1':
        for i in worlds_results:
            comp = jsonpickle.decode(i['results'])
            for k in comp:
                k['place'] = str(k['place'])
                if k['band'] not in output:
                    if k['place'] in coc_weightings:
                        output[k['band']] = coc_weightings[k['place']]
                    else:
                        output[k['band']] = 0
                else:
                    if k['place'] in coc_weightings:

                        output[k['band']] = output[k['band']] + coc_weightings[k['place']]

    new_output = []
    for key, value in output.items():
        new_output.append([key, value])

    quick_sort(new_output, 0, len(new_output)-1)
    return new_output


def get_drumming_coc(grade, year):

    results = pull_data(competitions_collection, {'Grade': grade, 'year': year})
    worlds_msr_results = pull_data(competitions_collection, {'Grade': '1MSR', 'year': year})
    worlds_med_results = pull_data(competitions_collection, {'Grade': '1MED', 'year': year})

    output = {}

    for i in results:
        comp = jsonpickle.decode(i['results'])
        for k in comp:
            if k['band'] not in output:
                if k['d'] in coc_weightings:
                    output[k['band']] = coc_weightings[k['d']]
                else:
                    output[k['band']] = 0
            else:
                if k['d'] in coc_weightings:
                    output[k['band']] = output[k['band']] + coc_weightings[k['d']]

    if grade == '1':
        for i in worlds_med_results:
            comp = jsonpickle.decode(i['results'])
            for k in comp:
                if k['band'] not in output:
                    if k['d'] in coc_weightings:
                        output[k['band']] = coc_weightings[k['d']]
                    else:
                        output[k['band']] = 0
                else:
                    if k['d'] in coc_weightings:
                        output[k['band']] = output[k['band']] + coc_weightings[k['d']]

        for i in worlds_msr_results:
            comp = jsonpickle.decode(i['results'])
            for k in comp:
                if k['band'] not in output:
                    if k['d'] in coc_weightings:
                        output[k['band']] = coc_weightings[k['d']]
                    else:
                        output[k['band']] = 0
                else:
                    if k['d'] in coc_weightings:
                        output[k['band']] = output[k['band']] + coc_weightings[k['d']]

    new_output = []
    for key, value in output.items():
        new_output.append([key, value])

    quick_sort(new_output, 0, len(new_output)-1)
    return new_output


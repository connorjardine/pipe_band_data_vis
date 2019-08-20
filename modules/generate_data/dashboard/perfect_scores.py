import jsonpickle
from modules.db.db import *

grades_list = ['2', '3a', '3b', '4a', '4b', 'juv', 'Nov', 'Nov%20A', 'Nov%20B']


def partition(arr, low, high, index):
    i = (low - 1)
    pivot = arr[high][index]

    for j in range(low, high):
        if arr[j][index] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high, index):
    if low < high:
        pi = partition(arr, low, high, index)
        quick_sort(arr, low, pi - 1, index)
        quick_sort(arr, pi + 1, high, index)


def convert_grade(grade):
    if grade == 'juv':
        grade = 'Juv'
    if grade == 'Nov%20A':
        grade = 'Nov A'
    if grade == 'Nov%20B':
        grade = 'Nov B'
    return grade


def get_perfect_scores():
    perfect = []
    perfect_totals = []
    results = pull_data(competitions_collection)
    for k in results:
        winning_band = jsonpickle.decode(k['results'])[0]
        if winning_band['band'] == "George Watson's College":
            winning_band['band'] = "George Watsons College"
        if winning_band['band'] == "St. Laurence O'Toole":
            winning_band['band'] = "St Laurence O'Toole - Eire"
        if winning_band['total'] == '4':
            perfect.append([k['year'], k['contest'], convert_grade(k['Grade']), winning_band['band']])

            existing_band = next((item for item in perfect_totals if item["band_name"] == winning_band['band']), False)
            if not existing_band:
                perfect_totals.append({'band_name': winning_band['band'], 'count': 1})
            else:
                existing_band['count'] += 1

    quick_sort(perfect_totals, 0, len(perfect_totals) - 1, 'count')
    perfect_totals.reverse()
    return perfect, perfect_totals


# push_data(helper_collection, {"type": "perfect_scores", "data": jsonpickle.encode((get_perfect_scores()))})

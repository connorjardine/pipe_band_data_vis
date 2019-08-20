from modules.db.db import *
import jsonpickle

worlds_data = pull_data(worlds_collection)


def new_worlds_format(result_type, worlds_data, worlds_collate):
    for k in jsonpickle.decode(worlds_data['results']):
        band_collate = list(filter(lambda band: band['band'] == k['band'], worlds_collate))
        if len(band_collate) == 0:
            if result_type == '1MSR':
                worlds_collate.append({'band': k['band'], 'final_t': int(k['total']), 'med_t': 0,
                                       'msr_t': int(k['total'])})
            else:
                worlds_collate.append({'band': k['band'], 'final_t': int(k['total']), 'med_t': int(k['total']),
                                       'msr_t': 0})
        else:
            band_collate[0]['final_t'] = band_collate[0]['final_t'] + int(k['total'])
            if result_type == '1MSR':
                band_collate[0]['msr_t'] = band_collate[0]['msr_t'] + int(k['total'])
            else:
                band_collate[0]['med_t'] = band_collate[0]['med_t'] + int(k['total'])
    return worlds_collate


data = pull_data(competitions_collection, {'year': 2019, 'Grade': '1MSR', 'contest': 'World Championships'})
result_type = '1MSR'
worlds_list = []
for i in data:
    worlds_list = new_worlds_format(result_type, i, worlds_list)

data = pull_data(competitions_collection, {'year': 2019, 'Grade': '1MED', 'contest': 'World Championships'})
result_type = '1MED'
for k in data:
    worlds_list = new_worlds_format(result_type, k, worlds_list)


sorted_worlds_list = sorted(worlds_list, key=lambda k: k['final_t'])
for i in range(len(sorted_worlds_list)):
    sorted_worlds_list[i]['place'] = i+1
new_dct = {'contest': 'World Championships', 'year': 2019, 'date': 'Saturday 17th August', 'Grade': '1',
           'results': jsonpickle.encode(sorted_worlds_list)}

# find_and_mod(worlds_collection, {'contest': 'World Championships', 'year': 2019, 'date': 'Saturday 17th August', 'Grade': '1'},
#             new_dct)

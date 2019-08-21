def convert_grade(grade):
    if grade == 'Juv':
        grade = 'juv'
    if grade == 'Nov A':
        grade = 'Nov%20A'
    if grade == 'Nov B':
        grade = 'Nov%20B'
    return grade


def convert_band_name(band):
    band_list = {'George Watsons College': "George Watson's College",
                 "George Watson's College - Juvenile": "George Watson's College",
                 'The House of Edgar - Shotts and Dykehead': 'Shotts and Dykehead Caledonia',
                 "St. Laurence O'Toole": "St Laurence O'Toole - Eire",
                 "St Laurence O'Toole": "St Laurence O'Toole - Eire",
                 'The House of Edgar Shotts and Dykehead': 'Shotts and Dykehead Caledonia',
                 'Simon Fraser University': 'Simon Fraser University - Canada',
                 'Boghall and Bathgate Caledonia': 'Peoples Ford - Boghall and Bathgate Caledonia',
                 'Greater Glasgow Police Pipe Band': 'Strathclyde Police',
                 'Buchan': 'Buchan Peterson'}
    if band in band_list:
        return band_list[band]
    return band


def add_to_dct(band, dct):
    band['band'] = convert_band_name(band['band'])
    if band['band'] not in dct:
        dct[band['band']] = {'1': 1}
    else:
        dct[band['band']]['1'] += 1
    return dct

import jsonpickle

from selenium import webdriver
import pymongo

client = pymongo.MongoClient("mongodb+srv://connor:Connor97@connor-5cmei.mongodb.net/test?retryWrites=true&w=majority")
db = client.rspba
competitions_collection = db.competitions
worlds_collection = db.worlds

grades_list = ['1', '2', '3a', '3b', '4a', '4b', 'juv', 'Nov%20A', 'Nov%20B']
pre_grades_list = ['1', '2', '3a', '3b', '4a', '4b', 'juv', 'Nov']
contests = ["British", "Scottish", "European", "United%20Kingdom", "World"]
pre_contests = ["British", "Scottish", "European", "Cowal", "World"]
driver = webdriver.Chrome()


def get_grade_data(year, grade, contest):

    if year < 2019:
        driver.get('https://www.rspba.org/results/displaybandcontestdetail.php?Year=' + str(year) + '&Contest=' + contest +
                   '%20Championships&Grade=' + str(grade))

        comp_raw = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[4]/td[2]/table/tbody/tr/td/font/p')
        comp_details = comp_raw.text.splitlines()
        if len(comp_details) == 13:
            comp_details += ['']

        bands = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[4]/td[2]/table/tbody/tr/td/font/table/tbody')
        comp = []
        for i in bands.find_elements_by_xpath('.//tr'):
            band_list = []
            for k in i.find_elements_by_xpath('.//td'):
                band_list.append(k.text)
            if band_list:
                comp.append({"band": band_list[0], "p1": band_list[2], "p2": band_list[3], "d": band_list[4],
                             "e": band_list[5], "total": band_list[6], "place": band_list[7]})

        if comp_details[7] is None:
            comp_details[7] = ""
            comp_details[8] = ""
            comp_details[9] = ""
            comp_details[10] = ""
            comp_details[11] = ""
            comp_details[12] = ""
            comp_details[13] = ""
        competitions_collection.insert_one({"contest": comp_details[1], "year": year, "date": comp_details[3],
                                            "Grade": grade,  "pj1": comp_details[7], "pj2": comp_details[9],
                                            "d": comp_details[11], "e": comp_details[13],
                                            "results": jsonpickle.encode(comp)})

        return "completed: " + str(year) + "    " + str(grade)
    else:
        driver.get(
            'https://www.rspba.org/results/displaybandcontestdetail.php?Year=' + str(year) + '&Contest=' + contest +
            '%20Championships&Grade=' + str(grade))

        comp_raw = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[3]/td[2]/table/tbody/tr/td/font/p')
        comp_details = comp_raw.text.splitlines()
        if len(comp_details) == 13:
            comp_details += ['']

        bands = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[3]/td[2]/table/tbody/tr/td/font/table/tbody')
        comp = []
        for i in bands.find_elements_by_xpath('.//tr'):
            band_list = []
            for k in i.find_elements_by_xpath('.//td'):
                band_list.append(k.text)
            if band_list:
                comp.append({"band": band_list[0], "p1": band_list[2], "p2": band_list[3], "d": band_list[4],
                             "e": band_list[5], "total": band_list[6], "place": band_list[7]})

        if comp_details[7] is None:
            comp_details[7] = ""
            comp_details[8] = ""
            comp_details[9] = ""
            comp_details[10] = ""
            comp_details[11] = ""
            comp_details[12] = ""
            comp_details[13] = ""
        competitions_collection.insert_one({"contest": comp_details[1], "year": year, "date": comp_details[3],
                                            "Grade": grade, "pj1": comp_details[7], "pj2": comp_details[9],
                                            "d": comp_details[11], "e": comp_details[13],
                                            "results": jsonpickle.encode(comp)})

        return "completed: " + str(year) + "    " + str(grade)


def get_worlds_results(year, event):
    if year < 2019:
        driver.get('https://www.rspba.org/results/displaybandcontestdetail.php?Year=' + str(
            year) + '&Contest=World%20Championships&Grade=1%20' + str(event))

        comp_raw = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[4]/td[2]/table/tbody/tr/td/font/p')

        bands = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[4]/td[2]/table/tbody/tr/td/font/table[1]')
        comp = []
        for i in bands.find_elements_by_xpath('.//tr'):
            band_list = []
            for k in i.find_elements_by_xpath('.//td'):
                band_list.append(k.text)
            if band_list:
                comp.append({"band": band_list[0], "p1": band_list[2], "p2": band_list[3], "d": band_list[4],
                             "e": band_list[5], "total": band_list[6], "place": band_list[7]})

        comp_details = comp_raw.text.splitlines()
        competitions_collection.insert_one({"contest": comp_details[1], "year": year, "date": comp_details[3],
                                            "Grade": "1" + event, "pj1": comp_details[7], "pj2": comp_details[9],
                                            "d": comp_details[11], "e": comp_details[13],
                                            "results": jsonpickle.encode(comp)})
        if event is 'MED':
            bands = driver.find_element_by_xpath(
                '//*[@id="Table1"]/tbody/tr[4]/td[2]/table/tbody/tr/td/font/table[2]/tbody')
            overall_comp = []
            counter = 1
            for i in bands.find_elements_by_xpath('.//tr'):
                band_list = []
                for k in i.find_elements_by_xpath('.//td'):
                    band_list.append(k.text)
                if band_list:
                    overall_comp.append({"band": band_list[0], "msr_t": band_list[1], "msr_p": band_list[2],
                                         "med_t": band_list[3], "med_p": band_list[4], "final_t": band_list[5],
                                         "place": counter})
                    counter += 1
            comp_details = comp_raw.text.splitlines()
            worlds_collection.insert_one({"contest": comp_details[1], "year": year, "date": comp_details[3],
                                          "Grade": "1", "pj1": comp_details[7], "pj2": comp_details[9],
                                          "d": comp_details[11], "e": comp_details[13],
                                          "results": jsonpickle.encode(overall_comp)})
    else:
        if event == 'FMSR':
            event = 'FRI%201%20MSR'
        elif event == 'FMED':
            event = 'FRI%201%20MED'
        else:
            event = '1%20' + str(event)
        driver.get('https://www.rspba.org/results/displaybandcontestdetail.php?Year=' + str(
            year) + '&Contest=World%20Championships&Grade=' + event)

        comp_raw = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[3]/td[2]/table/tbody/tr/td/font/p')

        bands = driver.find_element_by_xpath('//*[@id="Table1"]/tbody/tr[3]/td[2]/table/tbody/tr/td/font/table/tbody')
        comp = []
        for i in bands.find_elements_by_xpath('.//tr'):
            band_list = []
            for k in i.find_elements_by_xpath('.//td'):
                band_list.append(k.text)
            if band_list:
                comp.append({"band": band_list[0], "p1": band_list[2], "p2": band_list[3], "d": band_list[4],
                             "e": band_list[5], "total": band_list[6], "place": band_list[7]})

        comp_details = comp_raw.text.splitlines()
        competitions_collection.insert_one({"contest": comp_details[1], "year": year, "date": comp_details[3],
                                            "Grade": "1" + event, "pj1": comp_details[7], "pj2": comp_details[9],
                                            "d": comp_details[11], "e": comp_details[13],
                                            "results": jsonpickle.encode(comp)})


get_worlds_results(2019, 'FMSR')
# Scrape non-worlds data
'''
for i in range(2003, 2020)
    get_worlds_results(i, 'MED')
    get_worlds_results(i, 'MSR')
    if i < 2014:
        for k in pre_contests:
            for j in pre_grades_list:
                if j == '1' and k == "World":
                    continue
                else:
                    get_grade_data(i, j, k)
    else:
        for k in contests:
            if i < 2016:
                for j in pre_grades_list:
                    if j == '1' and k == "World":
                        continue
                    else:
                        get_grade_data(i, j, k)
            else:
                for j in grades_list:
                    if j == '1' and k == "World":
                        continue
                    else:
                        get_grade_data(i, j, k)
'''

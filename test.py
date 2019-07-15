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

    competitions_collection.insert_one({"contest": comp_details[1], "year": year, "date": comp_details[3],
                                        "Grade": grade,  "pj1": comp_details[7], "pj2": comp_details[9],
                                        "d": comp_details[11], "e": comp_details[13],
                                        "results": jsonpickle.encode(comp)})

    return "completed: " + str(year) + "    " + str(grade)


print(get_grade_data(2013, '4b', "European"))

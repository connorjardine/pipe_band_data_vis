from modules.db.db import *


def get_num_results():
    return len(list(pull_data(competitions_collection)))


def get_num_contest_sums():
    return list(pull_data(worlds_collection))


print(get_num_contest_sums()[0])
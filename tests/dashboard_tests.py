import jsonpickle

from modules.db.db import *
from modules.generate_data.dashboard.perfect_scores import get_perfect_scores
from modules.generate_data.dashboard.coc import get_coc, get_drumming_coc


def test_slams():
    slam_data = jsonpickle.decode(pull_data(helper_collection, {"type": "slams"})[0]['data'])
    assert slam_data is not []
    assert len(slam_data[0]) == 3


def test_perfect_scores():
    scores = get_perfect_scores()
    assert scores[0] is not []
    assert len(scores[0][0]) == 4
    assert scores[1] is not []
    assert len(scores[1][0]) == 2


def test_coc():
    coc_data = get_coc('1', 2017)
    assert coc_data is not []
    assert coc_data[-1][0] == 'Inveraray and District'
    assert coc_data[-1][1] == 29

    coc_data = get_coc('2', 2017)
    assert coc_data is not []
    assert coc_data[-1][0] == 'Lomond and Clyde'
    assert coc_data[-1][1] == 28

    coc_data = get_coc('1', 2003)
    assert coc_data is not []
    assert coc_data[-1][0] == 'Field Marshal Montgomery'
    assert coc_data[-1][1] == 25

    coc_data = get_coc('2', 2003)
    assert coc_data is not []
    assert coc_data[-1][0] == 'The Clan Gregor Society'
    assert coc_data[-1][1] == 29


def test_drumming_coc():
    coc_data = get_drumming_coc('1', 2017)
    assert coc_data is not []
    assert coc_data[-1][0] == 'Inveraray and District'
    assert coc_data[-1][1] == 31

    coc_data = get_drumming_coc('2', 2017)
    assert coc_data is not []
    assert coc_data[-1][0] == 'The Glasgow Skye Association'
    assert coc_data[-1][1] == 26

    coc_data = get_drumming_coc('1', 2003)
    assert coc_data is not []
    assert coc_data[-1][0] == 'The House of Edgar - Shotts and Dykehead'
    assert coc_data[-1][1] == 31

    coc_data = get_drumming_coc('2', 2003)
    assert coc_data is not []
    assert coc_data[-1][0] == 'The Clan Gregor Society'
    assert coc_data[-1][1] == 30

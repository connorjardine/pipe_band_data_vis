from modules.generate_data.worlds.worlds import get_grade1_worlds_totals, return_other_worlds_data


def test_g1_worlds_data():
    data = get_grade1_worlds_totals( 2003, 2019)
    assert len(data) != 0
    assert data is not []
    assert len(data[0][0]) == 2


def test_other_worlds_data():
    data = return_other_worlds_data('2', 2003, 2009)
    assert len(data) != 0
    assert data is not []
    assert len(data[0][0]) == 2


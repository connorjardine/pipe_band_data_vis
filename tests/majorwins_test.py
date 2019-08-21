from modules.generate_data.major_wins.get_results import get_band_results


def test_results():
    data = get_band_results('1', 'w', 2003, 2019)
    assert(data is not None)
    assert (len(data[0]) == 2)
    data = get_band_results('1', 'd', 2003, 2019)
    assert (data is not None)
    assert (len(data[0]) == 2)
    data = get_band_results('1', 'e', 2003, 2019)
    assert (data is not None)
    assert (len(data[0]) == 2)
    data = get_band_results('1', 'p', 2003, 2019)
    assert (data is not None)
    assert (len(data[0]) == 2)

    data = get_band_results('2', 'w', 2003, 2019)
    assert (data is not None)
    assert (len(data[0]) == 2)
    data = get_band_results('2', 'd', 2003, 2019)
    assert (data is not None)
    assert (len(data[0]) == 2)
    data = get_band_results('2', 'e', 2003, 2019)
    assert (data is not None)
    assert (len(data[0]) == 2)
    data = get_band_results('2', 'p', 2003, 2019)
    assert (data is not None)
    assert (len(data[0]) == 2)
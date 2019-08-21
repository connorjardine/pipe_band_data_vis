from modules.generate_data.band_results.band_results import get_bands_list
from modules.generate_data.band_results.band_results import update_band_data


def test_bands_list():
    data = get_bands_list('2', 2003, 2019)
    assert(len(data) != 0)
    data = get_bands_list('1', 2003, 2019)
    assert (len(data) != 0)
    data = get_bands_list('3a', 2003, 2019)
    assert (len(data) != 0)


def test_update_band_data():
    data = update_band_data('1', 'Field Marshal Montgomery', 'Inveraray and District', 2003, 2019)
    assert(data is not [[], []])
    assert(len(data[0]) == 4)
    assert(len(data[0][1]) == 3)
    assert(data[0][0][2] == 'Overall')
    data = update_band_data('1', 'Field Marshal Montgomery', 'none', 2003, 2019)
    assert (data is not [])

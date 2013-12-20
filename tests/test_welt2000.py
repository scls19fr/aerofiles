import pytest
from os import path
from aerofiles.formats import Welt2000Format, welt2000

FOLDER = path.dirname(path.realpath(__file__))
DATA_PATH = path.join(FOLDER, 'data', 'WELT2000.TXT')

data_available = pytest.mark.skipif(
    not path.exists(DATA_PATH),
    reason="requires WELT2000.TXT"
)


def test_comments():
    line = '$ this is a comment'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint is None


def test_parse_meiersberg():
    line = 'MEIER1 MEIERSBERG      #GLD!G 80133113012 164N511759E0065723DEP0'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'MEIERSBERG',
        'shortname': 'MEIER1',
        'icao': None,
        'classifiers': set([
            'airfield',
            'glidersite',
            'landable',
        ]),
        'runways': [
            {
                'surface': 'grass',
                'length': 800,
                'directions': [130, 310],
            },
        ],
        'frequencies': [
            {
                'frequency': '130.125',
            },
        ],
        'altitude': 164,
        'latitude': 51.29972222222222,
        'longitude': 6.956388888888889,
        'country': 'DE',
    }


def test_manosque():
    line = 'MANOSQ MANOSQUE PONT D907XDURANCE         295N434816E0054928FRQ0'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'MANOSQUE PONT D907XDURANCE',
        'shortname': 'MANOSQ',
        'classifiers': set([
            'bridge',
        ]),
        'altitude': 295,
        'latitude': 43.80444444444444,
        'longitude': 5.8244444444444445,
        'country': 'FR',
    }


def test_marcoux():
    line = 'MARCO2 MARCOUX CHAMP 8!*FL08S 2513131     694N440739E0061714FRP0'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'MARCOUX CHAMP 8',
        'shortname': 'MARCO2',
        'icao': None,
        'field_number': 8,
        'classifiers': set([
            'landable',
            'catalogued',
        ]),
        'runways': [
            {
                'surface': 'sand',
                'length': 250,
                'directions': [130],
            },
        ],
        'frequencies': [],
        'altitude': 694,
        'latitude': 44.1275,
        'longitude': 6.287222222222222,
        'country': 'FR',
    }


def test_sydney():
    line = 'SYDNE1 SYDNEY NSW KINSS#YSSYA395160712050   6S335646E1511038AUQ0'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'SYDNEY NSW KINSS',
        'shortname': 'SYDNE1',
        'icao': 'YSSY',
        'classifiers': set([
            'airfield',
            'landable',
        ]),
        'runways': [
            {
                'surface': 'asphalt',
                'length': 3950,
                'directions': [160, 340],
            },
            {
                'directions': [70, 250],
            },
        ],
        'frequencies': [
            {
                'frequency': '120.500',
            },
        ],
        'altitude': 6,
        'latitude': -33.94611111111111,
        'longitude': 151.1772222222222,
        'country': 'AU',
    }


def test_ulm():
    line = 'ULMHBF ULM H BF                           480N482358E0095859DEJ0'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'ULM H BF',
        'shortname': 'ULMHBF',
        'classifiers': set([
            'railway-station',
        ]),
        'altitude': 480,
        'latitude': 48.39944444444444,
        'longitude': 9.983055555555556,
        'country': 'DE',
    }


def test_vettweis():
    line = 'VETTW2 VETTWEISS SOLLER*ULM!G 38153312097 159N504451E0063402DEP0'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'VETTWEISS SOLLER',
        'shortname': 'VETTW2',
        'icao': None,
        'classifiers': set([
            'landable',
            'ulm',
        ]),
        'runways': [
            {
                'surface': 'grass',
                'length': 380,
                'directions': [150, 330],
            },
        ],
        'frequencies': [
            {
                'frequency': '120.975',
            },
        ],
        'altitude': 159,
        'latitude': 50.7475,
        'longitude': 6.567222222222222,
        'country': 'DE',
    }


def test_weisweiler():
    line = 'WEISWE WEISWEILER KW 1011FT WESTL KUEHLT  144N505023E0061922DEP5'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'WEISWEILER KW 1011FT WESTL KUEHLT',
        'shortname': 'WEISWE',
        'classifiers': set([
            'power-plant',
        ]),
        'altitude': 144,
        'latitude': 50.83972222222222,
        'longitude': 6.322777777777778,
        'country': 'DE',
    }


def test_eddl_n():
    line = 'EDDLN0 EDDLN0 EDDL N  PFLICHTMELDEPUNKT    28N512424E0064454DEQ4'
    waypoint = Welt2000Format.parse_waypoint(line)

    assert waypoint == {
        'name': 'EDDLN0 EDDL N PFLICHTMELDEPUNKT',
        'shortname': 'EDDLN0',
        'classifiers': set([
            'reporting-point',
        ]),
        'altitude': 28,
        'latitude': 51.406666666666666,
        'longitude': 6.748333333333333,
        'country': 'DE',
    }


@data_available
def test_original():
    with open(DATA_PATH) as f:
        for line in f:
            check_waypoint(line)


def check_waypoint(line):
    waypoint = Welt2000Format.parse_waypoint(line)

    if not waypoint:
        assert line.startswith('$') or line.strip() == ''
        return

    # Check name
    assert 'name' in waypoint
    assert not waypoint['name'].endswith(' ?')
    assert not waypoint['name'].endswith(' !')
    assert not waypoint['name'].endswith('+')

    assert 'shortname' in waypoint
    assert len(waypoint['shortname']) == 6

    assert 'classifiers' in waypoint
    assert isinstance(waypoint['classifiers'], set)

    if 'icao' in waypoint and waypoint['icao']:
        assert 'airfield' in waypoint['classifiers']

    if '*ULM' in line or '#ULM' in line or '# ULM' in line:
        assert 'ulm' in waypoint['classifiers']

    if 'runways' in waypoint:
        assert isinstance(waypoint['runways'], list)
        assert 0 <= len(waypoint['runways']) <= 2
        for runway in waypoint['runways']:
            assert isinstance(runway, dict)
            if 'surface' in runway:
                assert runway['surface'] in welt2000.SURFACES.values()
            if 'length' in runway:
                assert 0 < runway['length'] <= 9999
            if 'directions' in runway:
                assert isinstance(runway['directions'], list)
                assert 1 <= len(runway['directions']) <= 2

    if 'frequencies' in waypoint:
        assert isinstance(waypoint['frequencies'], list)
        assert 0 <= len(waypoint['frequencies']) <= 1
        for frq in waypoint['frequencies']:
            assert 'frequency' in frq
            assert len(frq['frequency']) == 7
            assert frq['frequency'][3] == '.'

    assert 'altitude' in waypoint
    assert -999 <= waypoint['altitude'] <= 9999

    assert 'latitude' in waypoint
    assert -90 <= waypoint['latitude'] <= 90

    assert 'longitude' in waypoint
    assert -180 <= waypoint['longitude'] <= 180

    assert 'country' in waypoint
    assert len(waypoint['country']) == 2

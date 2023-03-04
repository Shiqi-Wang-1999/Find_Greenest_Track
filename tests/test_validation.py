import pytest
from tracknaliser.load import load_tracksfile,query_tracks
import mock
from tracknaliser import load

# ------------- Test Validation -------------
# negative test
# ---- Test Load Function ----
def test_no_directory():
    with pytest.raises(OSError) as exception:
        json = load_tracksfile('tests/dd/ss')
    assert "File is not accessible." in str(exception.value)


def test_invalid_json():
    with pytest.raises(TypeError) as exception:
        json = load_tracksfile('tests/samples.csv')
    assert "Input data must be JSON." in str(exception.value)


def test_invalid_structure():
    with pytest.raises(KeyError) as exception:
        json = load_tracksfile('tests/test_used_without_necessary_key.json')
    assert "Missing keys in dictionary. Must have keys metadata and tracks." in str(exception.value)

    with pytest.raises(KeyError) as exception:
        json = load_tracksfile('tests/test_used_without_necessary_meta_key.json')
    assert "Missing data in dictionary. Metadata must have keys datetime, end, mapsize and elevation." in str(exception.value)

    with pytest.raises(KeyError) as exception:
        json = load_tracksfile('tests/test_used_without_necessary_tracks_key.json')
    assert "Missing data in track information. Must have keys cc, elevation, road and terrain." in str(exception.value)


# ---- Test Query Function ----
def test_query_tracks():
    with pytest.raises(TypeError) as exception:
        tracks_1 = query_tracks(end={10: 20})
    assert "Coordinate of end {10: 20} must be List or Tuple." in str(exception.value)

    with pytest.raises(ValueError) as exception:
        tracks_1 = query_tracks(end=(10, ))
    assert "Coordinate of end (10,) must be 2D." in str(exception.value)

    with pytest.raises(TypeError) as exception:
        tracks_1 = query_tracks(start=("1", 1))
    assert "Coordinate of start ('1', 1) must be integer." in str(exception.value)

    with pytest.raises(ValueError) as exception:
        tracks_1 = query_tracks(start=(-1, -1), save=False)
    assert "Coordinate of start (-1, -1) is outside of the maximum map size." in str(exception.value)

    with pytest.raises(ValueError) as exception:
        tracks_1 = query_tracks(end=(300, 300), save=False)
    assert "Coordinate of end (300, 300) is outside of the maximum map size." in str(exception.value)

    with pytest.raises(TypeError) as exception:
        tracks_1 = query_tracks(save=1)
    assert "Please input the steps straight, 'n_tracks' with int type, and 'save' with bool type." in str(exception.value)

    with pytest.raises(ValueError) as exception:
        tracks_1 = query_tracks(min_steps_straight=-1)
    assert "The value of steps straight and n_tracks should be positive integer." in str(exception.value)

    with pytest.raises(ValueError) as exception:
        tracks_1 = query_tracks(min_steps_straight=3, max_steps_straight=2)
    assert "max_steps_straight must be greater than min_steps_straight." in str(exception.value)


# ---- mock test ----
def test_fail_internet_connection():
    fail_send = mock.Mock(return_value=False)
    load.isConnected = fail_send
    with pytest.raises(ConnectionError) as exception:
        tracks_1 = query_tracks()
    assert "No Internet Connection." in str(exception.value)

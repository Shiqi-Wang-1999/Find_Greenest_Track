from tracknaliser.tracks import SingleTrack
from math import sqrt
from tracknaliser.load import load_tracksfile

# ------------- Test SingleTrack -------------
def test_chaincode2corner():
    track_1 = SingleTrack([2, 3], "11233344111", "llmmmmlrrrr", "pggppdddppg", [17,18,19,24,23,22,21,16,11,12,13,14])
    assert track_1.corners() == [(2, 3), (4, 3), (4, 4), (1, 4), (1, 2), (4, 2)]
    track_2 = SingleTrack([1, 1], "12121443", "llmmmmlr", "pggppddd", [17,18,19,24,23,22,21,16,11])
    assert track_2.corners() == [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 1), (3, 1)]


def test_single_track():
    # test functions co2(), distance() and time()
    track_1 = SingleTrack((1, 1), "212", "lmr", "pgd", [100, 150, 150, 100])
    d1 = sqrt(1 + ((150 - 100) / 1000) ** 2)
    d2 = sqrt(1 + ((150 - 150) / 1000) ** 2)
    d3 = sqrt(1 + ((150 - 100) / 1000) ** 2)
    consumption = (5.4 / 100) * 1 * 1 * 1.3 * d1 + \
                  (5.4 / 100) * 1.25 * 1.25 * 1 * d2 + \
                  (5.4 / 100) * 1.4 * 2.5 * 0.45 * d3
    co2 = consumption * 2.6391
    distance = d1 + d2 + d3
    time = d1/80 + d2/120 + d3/30
    assert round(co2, 14) == round(track_1.co2(), 14)
    assert time == track_1.time()
    assert distance == track_1.distance()

    track_2 = SingleTrack((1, 1), "2121441112321", "llmmmmlrrrlml", "pggppdddppgdd", [17,18,19,24,23,22,21,16,11,16,46,50,14,36])
    # len(a_track)
    assert len(track_2) == 14
    # test track_2.start
    assert track_2.start == (1, 1)
    # test track_2.cc
    assert track_2.cc == "2121441112321"
    # test track_2.road
    assert track_2.road == "llmmmmlrrrlml"
    # test track_2.terrain
    assert track_2.terrain == "pggppdddppgdd"
    # test track_2.elevation
    assert track_2.elevation == [17,18,19,24,23,22,21,16,11,16,46,50,14,36]
    # test print(track_2)
    assert str(track_2) == "<SingleTrack: starts at (1, 1) - 13 steps>"


# ------------- Test Tracks -------------
def test_tracks():
    tracks_1 = load_tracksfile('tests/short_tracks.json')
    # len(tracks)
    assert len(tracks_1) == 5
    # print(tracks)
    assert str(tracks_1) == "<Tracks: 5 from (2, 3) to (4, 2)>"
    # greenest(), fastest() and shortest()
    assert str(tracks_1.greenest()) == "<SingleTrack: starts at (2, 3) - 5 steps>"
    assert str(tracks_1.shortest()) == "<SingleTrack: starts at (2, 3) - 5 steps>"
    assert str(tracks_1.fastest()) == "<SingleTrack: starts at (2, 3) - 5 steps>"
    # get_track(x)
    assert str(tracks_1.get_track(0)) == "<SingleTrack: starts at (2, 3) - 11 steps>"
    assert str(tracks_1.get_track(1)) == "<SingleTrack: starts at (2, 3) - 9 steps>"
    assert str(tracks_1.get_track(2)) == "<SingleTrack: starts at (2, 3) - 7 steps>"
    # tracks.start, tracks.end, tracks.map_size and tracks.date
    assert tracks_1.start == (2, 3)
    assert tracks_1.end == (4, 2)
    assert tracks_1.map_size == (5, 5)
    assert tracks_1.date == "2021-12-11T21:12:20"
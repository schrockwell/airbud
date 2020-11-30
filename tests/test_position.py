from airbud.gps.position import Position
from micropyGPS import MicropyGPS

"""
TODO 2020-11-29 Thomas Eckert:
These tests work with the assumption that the user instantiated the MicropyGPS
with `location_formatting` set to "dd" as the Position class will throw an 
error on instantiation with a MicropyGPS object if it has a different value
for `location_formatting`.
We should cover that case down the road instead of crashing.
"""


def test_instantiating_position_with_default_MicopyGPS():
    # Given
    expected_latitude = 0
    expected_longitude = 0
    expected_altitude_m = 0
    expected_valid = False
    expected_speed_kmhr = 0
    expected_course = 0
    expected_satellites_in_use = 0

    mock_micropy_gps = MicropyGPS(location_formatting="dd")

    # When
    actual = Position(mock_micropy_gps)

    # Then
    assert expected_latitude == actual.latitude
    assert expected_longitude == actual.longitude
    assert expected_altitude_m == actual.altitude_m
    assert expected_valid == actual.valid
    assert expected_speed_kmhr == actual.speed_kmhr
    assert expected_course == actual.course
    assert expected_satellites_in_use == actual.satellites_in_use


def test_to_dict():
    # Given
    expected_latitude = 0
    expected_longitude = 0
    expected_altitude_m = 0
    expected_valid = False
    expected_speed_kmhr = 0
    expected_course = 0
    expected_satellites_in_use = 0

    mock_micropy_gps = MicropyGPS(location_formatting="dd")

    # When
    actual = Position(mock_micropy_gps).to_dict()

    # Then
    assert expected_latitude == actual["latitude"]
    assert expected_longitude == actual["longitude"]
    assert expected_altitude_m == actual["altitude_m"]
    assert expected_valid == actual["valid"]
    assert expected_speed_kmhr == actual["speed_kmhr"]
    assert expected_course == actual["course"]
    assert expected_satellites_in_use == actual["satellites_in_use"]

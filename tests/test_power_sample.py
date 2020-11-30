from airbud.power_sample import PowerSample
from datetime import datetime, timezone, timedelta


def test_initialize_default_powersample():
    # Given
    expected_timestamp = datetime.now(timezone.utc)
    expected_latitude = 0
    expected_longitude = 0
    expected_altitude_m = 0
    expected_dbfs = 0
    expected_look_az = 0
    expected_look_el = 0
    expected_look_range = 0
    expected_rx_antenna_gain = 0
    expected_fspl_db = 0

    # When
    actual = PowerSample()

    # Then
    assert abs(
        expected_timestamp - datetime.fromisoformat(actual.timestamp)
    ) < timedelta(seconds=1)
    assert expected_latitude == actual.latitude
    assert expected_longitude == actual.longitude
    assert expected_altitude_m == actual.altitude_m
    assert expected_dbfs == actual.dbfs
    assert expected_look_az == actual.look_az
    assert expected_look_el == actual.look_el
    assert expected_look_range == actual.look_range
    assert expected_rx_antenna_gain == actual.rx_antenna_gain
    assert expected_fspl_db == actual.fspl_db

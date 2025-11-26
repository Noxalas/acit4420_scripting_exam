import pytest
from courier_optimizer.delivery import Delivery


def test_valid_delivery_row():
    """A valid row should validate to True."""
    row = {
        "customer": "Alice Smith",
        "latitude": "49.2827",
        "longitude": "-123.1207",
        "priority": "High",
        "weight_kg": "2.5",
    }
    assert Delivery.validate(row) is True


def test_invalid_customer_nonprintable():
    """Customer name contains non-printable characters."""
    row = {
        "customer": "Bob\x00Smith",
        "latitude": "49.0",
        "longitude": "-123.0",
        "priority": "Medium",
        "weight_kg": "1",
    }
    assert Delivery.validate(row) is False


def test_invalid_priority():
    """Priority must be High, Medium, or Low."""
    row = {
        "customer": "Charlie",
        "latitude": "49.0",
        "longitude": "-123.0",
        "priority": "Urgent",
        "weight_kg": "1.0",
    }
    assert Delivery.validate(row) is False


@pytest.mark.parametrize(
    "lat,lon",
    [
        ("91", "0"),  # latitude too high
        ("-91", "0"),  # latitude too low
        ("0", "181"),  # longitude too high
        ("0", "-181"),  # longitude too low
    ],
)
def test_invalid_coordinates(lat, lon):
    """Latitude must be between −90 and 90, longitude between −180 and 180."""
    row = {
        "customer": "David",
        "latitude": lat,
        "longitude": lon,
        "priority": "Low",
        "weight_kg": "3.0",
    }
    assert Delivery.validate(row) is False


def test_invalid_latitude_non_numeric():
    row = {
        "customer": "Eve",
        "latitude": "north",
        "longitude": "-123.0",
        "priority": "High",
        "weight_kg": "3.0",
    }
    assert Delivery.validate(row) is False


def test_invalid_longitude_non_numeric():
    row = {
        "customer": "Frank",
        "latitude": "49.0",
        "longitude": "west",
        "priority": "Low",
        "weight_kg": "3.0",
    }
    assert Delivery.validate(row) is False


def test_invalid_weight_negative():
    row = {
        "customer": "George",
        "latitude": "50.0",
        "longitude": "-120.0",
        "priority": "Medium",
        "weight_kg": "-5",
    }
    assert Delivery.validate(row) is False


def test_invalid_weight_non_numeric():
    row = {
        "customer": "Helen",
        "latitude": "50.0",
        "longitude": "-120.0",
        "priority": "Medium",
        "weight_kg": "heavy",
    }
    assert Delivery.validate(row) is False

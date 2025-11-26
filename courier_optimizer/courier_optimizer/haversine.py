import math

EARTH_RADIUS_KM = 6371


def get_haversine_distance(
    latitude_degrees1: float,
    longitude_degrees1: float,
    latitude_degrees2: float,
    longitude_degrees2: float,
) -> float:
    """
    Computes the distance between two points on Earth using the haversine formula.

    All latitude/longitude values should be in degrees.
    Returns the distance in kilometers.
    """

    latitude1, longitude1, latitude2, longitude2 = map(
        math.radians,
        (latitude_degrees1, longitude_degrees1, latitude_degrees2, longitude_degrees2),
    )

    latitude_difference = latitude2 - latitude1
    longitude_difference = longitude2 - longitude1

    a = (
        math.sin(latitude_difference / 2) ** 2
        + math.cos(latitude1)
        * math.cos(latitude2)
        * math.sin(longitude_difference / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c

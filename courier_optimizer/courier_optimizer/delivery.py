import re


class Delivery:
    PRIORITY_WEIGHTS = {"High": 0.6, "Medium": 1.0, "Low": 1.2}

    def __init__(self, customer, latitude, longitude, priority, weight_kg):
        self.customer = customer
        self.latitude = latitude
        self.longitude = longitude
        self.priority = priority
        self.weight_kg = weight_kg

    @classmethod
    def validate(cls, row) -> bool:
        """Parses and validates CSV row data and returns a boolean"""

        customer = row["customer"]
        latitude = row["latitude"]
        longitude = row["longitude"]
        priority = row["priority"]
        weight = row["weight_kg"]

        if not all(c.isprintable() for c in customer):
            return False

        if not re.match(r"^(High|Medium|Low)$", priority):
            return False

        try:
            latitude, longitude = float(latitude), float(longitude)
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                return False
            weight = float(weight)
            if weight < 0:
                return False
        except ValueError:
            return False

        return True

from haversine import get_haversine_distance
from transport import TRANSPORT_MODES


def optimize_route(deliveries: list, transport_mode: str, criterion: str):
    if not deliveries:
        return []

    mode_data = TRANSPORT_MODES[transport_mode]
    speed = mode_data["speed"]
    cost_per_km = mode_data["cost"]
    co2_per_km = mode_data["co2"]

    if criterion not in ("time", "cost", "co2"):
        criterion = "time"

    route = []
    remaining = deliveries.copy()

    remaining.sort(key=lambda d: d.PRIORITY_WEIGHTS[d.priority], reverse=True)
    current = remaining.pop(0)
    route.append(current)

    while remaining:

        def score(next_delivery):
            distance = get_haversine_distance(
                float(current.latitude),
                float(current.longitude),
                float(next_delivery.latitude),
                float(next_delivery.longitude),
            )

            priority_factor = 1 / next_delivery.PRIORITY_WEIGHTS[next_delivery.priority]

            if criterion == "time":
                return (distance / speed) * priority_factor
            elif criterion == "cost":
                return (distance * cost_per_km) * priority_factor
            else:
                return (distance * co2_per_km) * priority_factor

        next_delivery = min(remaining, key=score)
        route.append(next_delivery)
        remaining.remove(next_delivery)
        current = next_delivery

    return route

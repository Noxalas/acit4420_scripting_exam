from haversine import get_haversine_distance
from delivery import Delivery
from transport import TRANSPORT_MODES


def optimize_route(
    deliveries: list[Delivery],
    depot_location: tuple[float, float],
) -> list[Delivery]:
    """
    Computes an optimized delivery route using the Weighted Nearest Neighbor heuristic.

    The heuristic prioritizes stops with a lower (weighted) distance score, where
    priority factors influence the selection order (e.g., High priority makes the
    effective distance smaller).

    Args:
        deliveries: List of Delivery objects to be routed.
        depot_location: Tuple (latitude, longitude) of the start/end depot.

    Returns:
        A list of Delivery objects representing the optimized route order.
    """
    if not deliveries:
        return []

    PRIORITY_WEIGHTS = Delivery.PRIORITY_WEIGHTS

    route = []
    remaining = deliveries.copy()

    current_lat, current_lon = depot_location

    while remaining:
        best_delivery = None
        min_weighted_distance = float("inf")

        for next_delivery in remaining:
            distance = get_haversine_distance(
                float(current_lat),
                float(current_lon),
                float(next_delivery.latitude),
                float(next_delivery.longitude),
            )

            priority_weight = PRIORITY_WEIGHTS.get(next_delivery.priority, 1.0)

            weighted_distance = distance * priority_weight

            if weighted_distance < min_weighted_distance:
                min_weighted_distance = weighted_distance
                best_delivery = next_delivery

        if best_delivery:
            route.append(best_delivery)
            remaining.remove(best_delivery)
            current_lat, current_lon = best_delivery.latitude, best_delivery.longitude
        else:
            break

    return route
